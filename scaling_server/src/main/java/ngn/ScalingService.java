package ngn;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;

import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.util.UriComponentsBuilder;
import okhttp3.*;

@Service
@Slf4j
public class ScalingService {
    private final OkHttpClient okHttpClient = new OkHttpClient();
    private final String createServerUrl = "http://172.17.0.1:1234/createServer";
    private final String removeServerUrl = "http://172.17.0.1:1234/removeServer";
    private final long start = 2;
    private final long max = 10;
    long current = 2;


    @Scheduled(fixedDelayString = "60000", initialDelay = 0)
    public void scaleUp() {
        long requestPerSecond = getRequestPerSecond();
        manageServers(requestPerSecond);
    }

    public long getRequestPerSecond() {
        long requestPerSecond = 0;

        // String query = "rate(http_client_requests_seconds_count{http_method='POST'}[2m])";
        String query = "increase(http_client_requests_seconds_count{http_method='POST'}[5m])";
        JsonNode result = queryPrometheus(query);
        log.info("Clear Result: {}", result.toString());
        for(JsonNode node : result) {
            requestPerSecond += node.get("value").get(1).asLong();
        }
        log.info("Result: {}", requestPerSecond);
        return requestPerSecond;
    }

    public JsonNode queryPrometheus(String query) {
        String prometheusUrl = "http://10.0.11.1:9090/api/v1/query";
        String url = prometheusUrl + "?query=" + query;
        Request request = new Request.Builder()
                .url(UriComponentsBuilder.fromUriString(url).toUriString())
                .header("Accept", "application/json")
                .build();

        try (Response response = okHttpClient.newCall(request).execute()){
            String jsonResponse = response.body().string();
            ObjectMapper objectMapper = new ObjectMapper();
            return objectMapper.readTree(jsonResponse).get("data").get("result");
        } catch (Exception e) {
            throw new RuntimeException("Error parsing Prometheus response", e);
        }
    }


    public void manageServers(long requestPerSecond) {
        long instances = start + requestPerSecond / 1000;
        log.info("Current {}, update to: {}", current, instances);
        if(instances > max) instances = max;

        if(instances > current) {
            for(long i = current; i < instances; i++) {
                createServer("server" + i, "10.0.2." + i);
            }
        }
        if(instances < current) {
            for(long i = instances; i < current; i++) {
                removeServer("server" + i, "10.0.2." + i);
            }
        }
        current = instances;
    }

    public void removeServer(String name, String ip) {
        manageServer(removeServerUrl, name, ip);
    }

    public void createServer(String name, String ip) {
        manageServer(createServerUrl, name, ip);
    }

    @Data
    public static class DataBody {
        private String name;
        private String ip;
    }

    public void manageServer(String url, String name, String ip) {
        Gson gson = new Gson();
        MediaType mediaType = MediaType.parse("application/json");
        DataBody dataBody = new DataBody();
        dataBody.setName(name);
        RequestBody body = RequestBody.create(mediaType, gson.toJson(dataBody));
        Request request = new Request.Builder()
                .url(url)
                .method("POST", body)
                .build();

        try (Response response = okHttpClient.newCall(request).execute()){
            String jsonResponse = response.body().string();
            log.info("Call {} response: {}", url, jsonResponse);
        } catch (Exception e) {
            throw new RuntimeException("Error parsing Prometheus response", e);
        }
    }
}

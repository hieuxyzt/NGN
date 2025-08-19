package ngn;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.util.UriComponentsBuilder;

@Service
@Slf4j
public class ScalingService {
    private final OkHttpClient okHttpClient = new OkHttpClient();

    @Scheduled(fixedDelayString = "10000", initialDelay = 0)
    public void scaleUp() {
        long requestPerSecond = 0;

        String query = "rate(http_client_requests_seconds_count{method='POST'}[5m])";
        JsonNode result = queryPrometheus(query);
        log.info("Clear Result: {}", result.toString());
        for(JsonNode node : result) {
            requestPerSecond += node.get("value").get(1).asLong();
        }
        log.info("Result: {}", requestPerSecond);
    }

    public JsonNode queryPrometheus(String query) {
        String prometheusUrl = "http://localhost:9090/api/v1/query";
        String url = prometheusUrl + "?query=" + query;
        Request requestBuilder = new Request.Builder()
                .url(UriComponentsBuilder.fromUriString(url).toUriString())
                .header("Accept", "application/json")
                .build();

        try (Response response = okHttpClient.newCall(requestBuilder).execute()){
            String jsonResponse = response.body().string();
            ObjectMapper objectMapper = new ObjectMapper();
            return objectMapper.readTree(jsonResponse).get("data").get("result");
        } catch (Exception e) {
            throw new RuntimeException("Error parsing Prometheus response", e);
        }
    }
}

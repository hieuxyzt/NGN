package ngn;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@Slf4j
public class ScalingService {
    private final RestTemplate restTemplate = new RestTemplate();

    @Scheduled(fixedDelayString = "10000", initialDelay = 0)
    public void scaleUp() {
        JsonNode result = queryPrometheus("up");
        log.info(result.toString());
    }

    public JsonNode queryPrometheus(String query) {
        String prometheusUrl = "http://localhost:9090/api/v1/query";
        String url = prometheusUrl + "?query=" + query;
        String jsonResponse = restTemplate.getForObject(url, String.class);
        log.info(jsonResponse);

        try {
            ObjectMapper objectMapper = new ObjectMapper();
            log.info(objectMapper.readTree(jsonResponse).get("data").toString());
            return objectMapper.readTree(jsonResponse).get("data").get("result");
        } catch (Exception e) {
            throw new RuntimeException("Error parsing Prometheus response", e);
        }
    }
}

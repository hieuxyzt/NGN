package ngn;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ServerController {
    @GetMapping("/")
    private String home() {
        return "Hello World";
    }
    @GetMapping("/hello/{id}")
    private String hello(@PathVariable String id) {
        return "Hello " + (id + 1);
    }
}

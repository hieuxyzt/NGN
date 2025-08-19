package ngn;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ServerController {
    @GetMapping("/")
    private String home() {
        return "Hello World";
    }

    @PostMapping("/")
    private String hello() {
        return "Hello World";
    }
}

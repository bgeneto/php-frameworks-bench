import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
    thresholds: {
        http_req_failed: [{ threshold: "rate<0.01" }]
    },
    scenarios: {
        breaking: {
            executor: "ramping-vus",
            stages: [
                { duration: "10s", target: 100 },
                { duration: "10s", target: 200 },
                { duration: "10s", target: 300 },
                { duration: "10s", target: 500 },
                { duration: "10s", target: 750 },
                { duration: "10s", target: 1000 },
            ],
        },
    },
};

export default function () {
    http.get('{{ URI }}');
    sleep(0.5);
}


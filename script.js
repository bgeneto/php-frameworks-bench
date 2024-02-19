import http from 'k6/http';
import { sleep } from 'k6';
export const options = {
  vus: ,
  duration: '',
};
export default function () {
  http.get('300');
  sleep();
}

import init, { calculate_proof } from './pkg/susctf_pow.js';

self.report_rate = function (rate) {
    self.postMessage({
        type: "msg",
        value: "Current rate: " + rate + "k hashes/s"
    });
};

onmessage = function ({ data }) {
    const { answer, token, difficulty } = data

    init().then(() => {
        const proof = calculate_proof(answer, token, difficulty)
        postMessage({
            type: "result",
            value: proof
        })
    })
}

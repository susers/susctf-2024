import { randomInt } from "node:crypto";

interface Context {
  startTime: number;
  requestIdx: number;
}

interface RequestInformation {
  status: number;
  rawText: string;
}

const timerQueue = new Array<Context>();
let correctCount = 0;

async function loadRequests(): Promise<Array<RequestInformation>> {
  const files = [];
  for await (const dirEntry of Deno.readDir("requests")) {
    if (dirEntry.isFile && dirEntry.name.endsWith(".txt")) {
      files.push(dirEntry.name);
    }
  }
  const requests: Array<RequestInformation> = [];
  for (const file of files) {
    const content = await Deno.readTextFile(`requests/${file}`);
    requests.push({
      status: Number(file.split(".")[0]),
      rawText:
        content
          .trim()
          .replaceAll("RANDOM_STR", crypto.randomUUID().replace(/-/g, ""))
          .replaceAll("RANDOM_INT", String(randomInt(2 << 8, 2 << 16)))
          .replaceAll("\n", "\r\n") + "\r\n\r\n",
    });
  }
  return requests;
}

const requests: Array<RequestInformation> = await loadRequests();
const flag = Deno.env.get("GZCTF_FLAG") || "susctf{testflag}";
const PORT = 8080;
const TIMEOUT_PERIOD = 1000;
const SUCC_COUNT = 100;

function sendRandomRequest(sock: WebSocket) {
  const startTime = Date.now();
  const idx = randomInt(requests.length);
  const randomRequest = requests[idx];
  sock.send(randomRequest.rawText);
  timerQueue.push({
    startTime,
    requestIdx: idx,
  });
}

function verify(r: string, idx: number): boolean {
  return requests[idx].status === Number(r);
}

async function handleRequest(req: Request): Promise<Response> {
  const { pathname } = new URL(req.url);

  if (pathname === "/ws") {
    if (req.headers.get("upgrade") === "websocket") {
      const { socket, response } = Deno.upgradeWebSocket(req);

      socket.onopen = () => {
        console.log("CONNECTED");
        sendRandomRequest(socket);
      };
      socket.onmessage = (event: MessageEvent) => {
        console.log(`RECEIVED: ${event.data}`);
        const ctx: Context | undefined = timerQueue.pop();
        const curTime = Date.now();
        if (ctx !== undefined && verify(event.data, ctx.requestIdx)) {
          if (curTime - ctx.startTime >= TIMEOUT_PERIOD) {
            console.log("TIMEOUT");
            socket.send("Timeout!");
            correctCount = 0;
            return response;
          }
          console.log("OK");
          correctCount++;
          if (correctCount < SUCC_COUNT) {
            sendRandomRequest(socket);
          } else {
            console.log("FINISH");
            socket.send("Congratulations!\nFlag is " + flag);
            correctCount = 0;
            socket.close();
          }
        } else {
          console.log("WRONG");
          socket.send("Wrong answer!");
          correctCount = 0;
        }
      };
      socket.onclose = () => console.log("DISCONNECTED");
      socket.onerror = (error) => console.error("ERROR: ", error);

      return response;
    }
  }

  if (pathname === "/") {
    const html = await Deno.readTextFile("index.html");
    return new Response(html, {
      headers: { "content-type": "text/html" },
    });
  }

  return new Response("Not Found", { status: 404 });
}

Deno.serve({ port: PORT, handler: handleRequest });

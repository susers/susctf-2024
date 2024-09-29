const express = require("express");
const cookieParser = require("cookie-parser");
const fs = require("fs");
const ejs = require("ejs");
const path = require("path");
const fileUpload = require("express-fileupload");
const { randomUUID } = require("crypto");
const { visit } = require("./bot");
const flag_id = randomUUID();
const maxLength = 1024;
const port = 3000;

const checkUUID = (uuid) => {
  return /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(
    uuid,
  );
};

const plantflag = () => {
  fs.mkdirSync(path.join(__dirname, `/public/${flag_id}`));
  fs.writeFileSync(
    path.join(__dirname, `/public/${flag_id}/flag.txt`),
    process.env.GZCTF_FLAG || "susctf{test}",
  );
};

const app = express();

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(cookieParser());
app.use(fileUpload());
app.use(express.json());

app.get("/", async (req, res) => {
  if (req.cookies.uid && checkUUID(req.cookies.uid)) {
    try {
      const files = btoa(
        JSON.stringify(
          fs.readdirSync(path.join(__dirname, `/public/${req.cookies.uid}`)),
        ),
      );
      return res.render("index", { files: files, id: req.cookies.uid });
    } catch (err) {}
  }

  let uid = randomUUID();
  fs.mkdirSync(path.join(__dirname, `/public/${uid}`));
  return res.cookie("uid", uid).render("index", { files: null, id: uid });
});

app.post("/add_note", async (req, res) => {
  if (
    !req.body.content ||
    !req.body.title ||
    !req.cookies.uid ||
    typeof req.body.content !== "string" ||
    typeof req.body.title !== "string" ||
    !checkUUID(req.cookies.uid)
  ) {
    return res.status(400).send("Invalid request");
  }
  try {
    const content = req.body.content;
    const title = req.body.title;
    if (content.length > maxLength) {
      return res.status(400).send("Note length exceeds the limit.");
    }
    fs.writeFileSync(`./public/${req.cookies.uid}/${title}`, content);
  } catch {
    return res.status(400).send("Invalid request");
  }

  return res.status(200).redirect("/");
});

app.post("/share", async (req, res) => {
  let id = req.body.id;
  let title = req.body.title;
  await visit(flag_id, id, title);
  return res.send("Success!");
});

app.listen(port, () => {
  plantflag();
  console.log(`Server is running on port ${port}`);
});
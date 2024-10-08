const express = require("express")
const port = process.env.PORT || 8001;
const app = express();

app.use(express.static(__dirname + "/build/"));
app.get(/.*/, function(req, res) {
    res.sendFile(__dirname + "/build/index.html");
});
app.listen(port);

console.log("Server started")
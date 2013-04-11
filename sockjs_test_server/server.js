
// Require
var sockjs = require("sockjs");
var _ = require("underscore");
var http = require("http");


// SockJs server
var listeners = [];
function hookupCallbacks(conn) {
    conn.on('data',
        function (message) {
            console.log("Data received: ", message);
            if (message == 'iamlistener') {
                console.log("Added listener: ", conn.url);
                listeners.push(conn);
            } else if (message == 'echome') {
                conn.write("echo: " + message);
                for (var index in listeners) {
                    listeners[index].send(message);
                }
            } else {
                console.log("Message: ", message);
                for (var index in listeners) {
                    listeners[index].send(message);
                }
            }
        });

    conn.on('close',
        function () {
            console.log("Connection closed");
        });
}
var logger = function(level, msg) {
    console.log("> ", level, ": ", msg);
}
var sock_server = sockjs.createServer({websocket: true});
sock_server.on('connection', function(conn) {
    console.log("New connection: url=", conn.url, " protocol=", conn.protocol);
    hookupCallbacks(conn);
});

// Http server
var http_server = http.createServer();
sock_server.installHandlers(http_server, {prefix:'/socket.io'});

http_server.on('request',
                function (req, res) {
                    if (req.url == '/web_client') {
                        renderWebClientPage(res);
                    }
                });

var web_client_page_cache = null;
function renderWebClientPage(res) {
    if (web_client_page_cache == null) {
        var fs = require('fs');
        fs.readFile('./web_client.html', 'utf8', function(err, data) {
            if (err !== null) {
                console.log("Failed to read file: ", err);
                return;
            }

            web_client_page_cache = data;
            renderWebClientPage(res);
        });
        return;
    }

    res.writeHead(200, {'Content-Length': web_client_page_cache.length,
                        'Content-Type': 'text/html' });

    res.write(web_client_page_cache);
    res.end();

    web_client_page_cache = null;
}

// Start
http_server.listen(9999, '0.0.0.0');


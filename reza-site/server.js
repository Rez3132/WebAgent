const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const chunksDir = path.join(__dirname, 'chunks');

function buildHtml() {
  return fs.readdirSync(chunksDir)
    .filter(name => name.endsWith('.txt'))
    .sort()
    .map(name => fs.readFileSync(path.join(chunksDir, name), 'utf8'))
    .join('');
}

const html = buildHtml();

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, {'Content-Type': 'text/plain; charset=utf-8'});
    return res.end('ok');
  }

  res.writeHead(200, {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'public, max-age=300'
  });
  res.end(html);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Reza site listening on port ${PORT}`);
});

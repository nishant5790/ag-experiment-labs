const fetch = require('node-fetch');

async function test() {
  const params = new URLSearchParams();
  params.append('message', 'AI trends in 2026');
  params.append('stream', 'false');

  const res = await fetch('http://localhost:8000/workflows/content-creation-workflow/runs', {
    method: 'POST',
    body: params
  });
  const data = await res.json();
  console.log(JSON.stringify(data, null, 2));
}

test();

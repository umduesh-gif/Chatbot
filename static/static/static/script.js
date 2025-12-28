async function send() {
  const msg = document.getElementById("msg").value;
  const persona = document.getElementById("persona").value;
  const nsfw = document.getElementById("nsfw").checked;

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ message: msg, persona, nsfw })
  });

  const data = await res.json();

  document.getElementById("out").innerText =
    data.angel + "\n\n" + data.demon;
}

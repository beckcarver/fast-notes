const API_BASE = "/api/v1/notes";  // ✅ must match FastAPI router prefix

async function getNotes() {
    const res = await fetch(API_BASE);
    const notes = await res.json();
    const ul = document.getElementById("notes");
    ul.innerHTML = "";
    notes.forEach(note => {
        const li = document.createElement("li");
        li.className = "note";
        li.textContent = `${note.id}: ${note.title} - ${note.content}`;
        
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.onclick = () => deleteNote(note.id);
        li.appendChild(deleteBtn);
        
        ul.appendChild(li);
    });
}

async function createNote() {
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").value;

  if (!title || !content) return;

  await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, content }),
  });

  document.getElementById("title").value = "";
  document.getElementById("content").value = "";
  getNotes();
}

async function deleteNote(id) {
  await fetch(`${API_BASE}/${id}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id }),
  });
  getNotes();
}

window.onload = getNotes;
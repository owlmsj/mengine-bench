(function () {
"use strict";
var root = document.getElementById("qm-root");
var AT = document.querySelector('meta[name="qm-at"]').getAttribute("content");
var ME = null;
var VIEWS = [["inbox", "INBOX", "Inbox"], ["starred", "STARRED", "Starred"], ["sent", "SENT", "Sent"], ["all", "ALL", "All Mail"], ["trash", "TRASH", "Trash"]];
var query = "";
function esc(s) {
return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c];
});
}
function api(path, body) {
var opts = {credentials: "same-origin", headers: {}};
if (body !== undefined) {
opts.method = "POST";
opts.headers["Content-Type"] = "application/json";
opts.headers["X-Qm-At"] = AT;
opts.body = JSON.stringify(body);
}
return fetch(path, opts).then(function (r) {
return r.json().then(function (j) {
if (!r.ok) {
throw new Error(j.message || ("HTTP " + r.status));
}
return j;
});
});
}
function toast(text) {
var t = document.createElement("div");
t.className = "qm-toast";
t.setAttribute("role", "status");
t.textContent = text;
document.body.appendChild(t);
setTimeout(function () { t.remove(); }, 2500);
}
function shortDate(iso) {
var d = new Date(iso);
return d.toLocaleDateString("en-GB", {day: "numeric", month: "short"});
}
function route() {
var h = (location.hash || "#inbox").slice(1).split("/");
var v = VIEWS.filter(function (x) { return x[0] === h[0]; })[0] || VIEWS[0];
return {view: v, thread: h[1] || null};
}
function shell(r, inner) {
var nav = VIEWS.map(function (v) {
var n = v[1] === "INBOX" && ME ? ME.labels.INBOX : 0;
return '<a href="#' + v[0] + '" class="' + (v === r.view ? "on" : "") + '"><span>' + v[2] + "</span><span>" + (n || "") + "</span></a>";
}).join("");
root.innerHTML = '<header class="qm-top"><div class="qm-logo"><b>Q</b>uillmail</div>' +
'<form class="qm-search" role="search"><input name="q" aria-label="Search mail" placeholder="Search mail" value="' + esc(query) + '"></form>' +
'<div class="qm-account" title="Bench Tester (tester@quillmail.test)">B</div></header>' +
'<div class="qm-body"><nav class="qm-nav"><button class="qm-compose" disabled title="Compose is not part of this test account">Compose</button>' + nav + "</nav>" +
'<main class="qm-main">' + inner + "</main></div>";
root.querySelector(".qm-search").addEventListener("submit", function (e) {
e.preventDefault();
query = e.target.q.value;
location.hash = "#all";
render();
});
}
function renderList(r) {
var url = "/mail/api/threads?label=" + r.view[1] + (query ? "&q=" + encodeURIComponent(query) : "");
return api(url).then(function (res) {
var rows = res.threads.map(function (t) {
var who = t.from.map(function (p) { return p.email === ME.email ? "me" : (p.name || p.email).split(" ")[0]; }).join(", ");
var unread = t.labels.indexOf("UNREAD") >= 0;
return '<div class="qm-row' + (unread ? " unread" : "") + '" role="link" tabindex="0" data-id="' + t.id + '">' +
"<span>" + esc(who) + (t.count > 1 ? " " + t.count : "") + "</span>" +
'<span class="snip"><span class="subj">' + esc(t.subject) + "</span> - " + esc(t.snippet) + (t.hasAttachment ? '<span class="clip" title="Has attachment">&#128206;</span>' : "") + "</span>" +
'<span class="date">' + esc(shortDate(t.date)) + "</span></div>";
}).join("");
shell(r, '<div class="qm-bar"><button data-act="refresh" title="Refresh">&#8635; Refresh</button><span style="margin-left:auto;color:#5f6368">' + res.threads.length + " conversations</span></div>" +
(rows || '<div class="qm-empty">No conversations in ' + esc(r.view[2]) + ".</div>"));
root.querySelectorAll(".qm-row").forEach(function (row) {
var open = function () { location.hash = "#" + r.view[0] + "/" + row.getAttribute("data-id"); };
row.addEventListener("click", open);
row.addEventListener("keydown", function (e) { if (e.key === "Enter") { open(); } });
});
root.querySelector('[data-act="refresh"]').addEventListener("click", render);
});
}
function modify(id, add, remove) {
return api("/mail/api/thread/" + id + "/modify", {addLabels: add, removeLabels: remove});
}
function renderThread(r) {
return api("/mail/api/thread/" + r.thread).then(function (t) {
var opened = t.labels.indexOf("UNREAD") >= 0 ? modify(t.id, [], ["UNREAD"]) : Promise.resolve();
var first = t.messages[0];
var msgs = t.messages.map(function (m) {
var atts = m.attachments.map(function (a) {
var href = "/mail/u/0/attachment?th=" + t.id + "&att=" + a.id;
return '<a class="qm-att" href="' + href + '" download="' + esc(a.filename) + '" title="Download ' + esc(a.filename) + '"><span class="pdf">PDF</span>' + esc(a.filename) + ' <small>' + Math.round(a.size / 102.4) / 10 + " KB</small></a>";
}).join("");
return '<div class="qm-msg"><span class="when">' + esc(new Date(m.date).toLocaleString("en-GB")) + "</span>" +
'<span class="who">' + esc(m.from.name || m.from.email) + '</span> <span class="addr">&lt;' + esc(m.from.email) + "&gt;</span>" +
'<div class="addr">to ' + esc(m.to.map(function (p) { return p.email === ME.email ? "me" : p.email; }).join(", ")) + "</div>" +
"<pre>" + esc(m.body) + "</pre>" + (atts ? '<div class="qm-atts">' + atts + "</div>" : "") + "</div>";
}).join("");
var labels = t.labels.filter(function (l) { return l !== "UNREAD" && l !== "SENT"; }).map(function (l) { return '<span class="qm-label">' + (l === "INBOX" ? "Inbox" : l.charAt(0) + l.slice(1).toLowerCase()) + "</span>"; }).join("");
var last = t.messages[t.messages.length - 1];
var replyTo = last.from.email === ME.email ? last.to[0].email : last.from.email;
shell(r, '<div class="qm-bar"><button data-act="back" title="Back">&#8592;</button>' +
(t.labels.indexOf("INBOX") >= 0 ? '<button data-act="archive" title="Archive">Archive</button>' : '<button data-act="unarchive" title="Move to Inbox">Move to Inbox</button>') +
'<button data-act="trash" title="Delete">Delete</button><button data-act="unread" title="Mark as unread">Mark as unread</button>' +
'<button data-act="star" title="Star">' + (t.labels.indexOf("STARRED") >= 0 ? "Unstar" : "Star") + "</button></div>" +
'<div class="qm-thread"><h2>' + esc(t.subject) + labels + "</h2>" + msgs +
'<div class="qm-actions"><button data-act="reply">&#8617; Reply</button></div></div>');
var back = function () { location.hash = "#" + r.view[0]; };
var act = function (name, fn) { root.querySelector('[data-act="' + name + '"]').addEventListener("click", fn); };
act("back", back);
if (t.labels.indexOf("INBOX") >= 0) {
act("archive", function () { modify(t.id, [], ["INBOX"]).then(function () { toast("Conversation archived."); back(); }); });
} else {
act("unarchive", function () { modify(t.id, ["INBOX"], ["TRASH"]).then(function () { toast("Conversation moved to Inbox."); render(); }); });
}
act("trash", function () { modify(t.id, ["TRASH"], ["INBOX"]).then(function () { toast("Conversation moved to Trash."); back(); }); });
act("unread", function () { modify(t.id, ["UNREAD"], []).then(back); });
act("star", function () { var on = t.labels.indexOf("STARRED") >= 0; modify(t.id, on ? [] : ["STARRED"], on ? ["STARRED"] : []).then(render); });
act("reply", function () {
var box = document.createElement("form");
box.className = "qm-reply";
box.innerHTML = '<div class="to">To: ' + esc(replyTo) + '</div><textarea name="body" aria-label="Message Body"></textarea>' +
'<button class="qm-send" type="submit">Send</button>';
root.querySelector(".qm-actions").replaceWith(box);
box.body.focus();
box.addEventListener("submit", function (e) {
e.preventDefault();
api("/mail/api/send", {threadId: t.id, inReplyTo: last.id, to: [replyTo], subject: "Re: " + first.subject.replace(/^Re: /, ""), body: box.body.value}).then(function () {
toast("Message sent.");
render();
}, function (err) { toast(err.message); });
});
});
return opened;
});
}
function render() {
var r = route();
var go = function () { return r.thread ? renderThread(r) : renderList(r); };
return api("/mail/api/me").then(function (me) { ME = me; return go(); }).catch(function (err) {
root.innerHTML = '<div class="qm-empty">Something went wrong: ' + esc(err.message) + "</div>";
});
}
window.addEventListener("hashchange", render);
render();
})();

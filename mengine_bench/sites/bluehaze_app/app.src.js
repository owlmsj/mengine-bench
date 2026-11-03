// Bluehaze web client, source of the bundle `minify.py` builds into the workspace (#153). Fictional site.
// Written for the bundler: semicolons everywhere, no regex literals, no shorthand properties.
"use strict";

const mainColumn = document.getElementById("main");
const layerRoot = document.getElementById("layers");
const bootMeta = document.querySelector("meta[name=" + S("bh-boot") + "]");
let session = null;

// The write token the server expects, derived from this page load's nonce.
function writeToken(nonce) {
  let hash = 0x811c9dc5;
  let token = "";
  for (let round = 0; round < 4; round++) {
    const seed = nonce + "." + round;
    for (let index = 0; index < seed.length; index++) {
      hash ^= seed.charCodeAt(index);
      hash = Math.imul(hash, 0x01000193) >>> 0;
    }
    token += ("00000000" + hash.toString(16)).slice(-8);
  }
  return token;
}

const pageToken = writeToken(bootMeta ? bootMeta.getAttribute("content") : "");

function el(tag, attrs, ...kids) {
  const node = document.createElement(tag);
  for (const [name, value] of Object.entries(attrs || {})) {
    if (name.startsWith("on")) node.addEventListener(name.slice(2), value);
    else if (value !== null && value !== undefined && value !== false) node.setAttribute(name, value === true ? "" : value);
  }
  for (const kid of kids.flat()) if (kid !== null && kid !== undefined) node.append(kid);
  return node;
}

async function callApi(method, params, body, contentType) {
  const query = params ? "?" + new URLSearchParams(params) : "";
  const headers = {};
  let init = {credentials: "same-origin"};
  if (body !== undefined) {
    headers["Content-Type"] = contentType || "application/json";
    headers[S("X-Bh-Token")] = pageToken;
    init = {method: "POST", credentials: "same-origin", headers: headers, body: contentType ? body : JSON.stringify(body)};
  }
  const reply = await fetch(S("/xrpc/") + method + query, init);
  const payload = await reply.json();
  if (!reply.ok) throw new Error(payload.message || payload.error || reply.status);
  return payload;
}

function toast(message) {
  const box = document.getElementById("toast");
  box.textContent = message;
  box.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(function () { box.hidden = true; }, 3000);
}

function rkeyOf(uri) { return uri.split("/").pop(); }
function postPath(view) { return "/profile/" + view.author.handle + "/post/" + rkeyOf(view.uri); }
function navigate(path) { history.pushState(null, "", path); render(); }
function stamp(iso) { return new Date(iso).toLocaleString("en-US", {month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"}); }
function followLink(event) { event.preventDefault(); navigate(event.currentTarget.getAttribute("href")); }
function closeMenus() { document.querySelectorAll(".menu").forEach(function (menu) { menu.remove(); }); }

function postItem(view, opts) {
  const own = session && view.author.handle === session.handle;
  const reply = view.record.reply;
  const images = (view.embed && view.embed.images) || [];
  const item = el("div", {class: "post" + (opts.focus ? " focus" : ""), role: opts.focus ? null : "link",
      "data-testid": (opts.focus ? "postThreadItem-by-" : "feedItem-by-") + view.author.handle,
      "data-post-uri": view.uri, tabindex: opts.focus ? null : "0",
      onclick: function (event) { if (!opts.focus && !event.target.closest("a,button,.menu")) navigate(postPath(view)); }},
    el("div", {class: "meta"},
      el("a", {href: "/profile/" + view.author.handle, "aria-label": view.author.displayName, onclick: followLink},
        el("strong", {}, view.author.displayName)), " ",
      el("span", {class: "handle"}, "@" + view.author.handle), " · ",
      el("time", {datetime: view.indexedAt}, el("a", {href: postPath(view), onclick: followLink,
        "aria-label": view.record.text.slice(0, 40) || "Post", "data-tooltip": view.indexedAt}, stamp(view.indexedAt)))),
    reply ? el("div", {class: "context"}, "Reply to " + (opts.parentName || "a post")) : null,
    el("div", {class: "text", "data-testid": "postText"}, view.record.text),
    images.length ? el("div", {class: "images"}, images.map(function (image) { return el("img", {src: image.thumb, alt: image.alt}); })) : null,
    el("div", {class: "actions"},
      el("button", {class: "icon", type: "button", "data-testid": "replyBtn",
        "aria-label": "Reply (" + view.replyCount + (view.replyCount === 1 ? " reply)" : " replies)"),
        onclick: function () { openComposer(view); }}, "Reply " + view.replyCount),
      el("button", {class: "icon", type: "button", "data-testid": "postDropdownBtn", "aria-label": "Open post options menu",
        "aria-haspopup": "menu", onclick: function (event) { openMenu(item, view, own, event.currentTarget); }}, "...")));
  return item;
}

function openMenu(item, view, own, button) {
  closeMenus();
  const menu = el("div", {class: "menu", role: "menu", "aria-label": "Post options"},
    el("button", {role: "menuitem", type: "button", "data-testid": "postDropdownCopyTextBtn",
      onclick: function () { if (navigator.clipboard) navigator.clipboard.writeText(view.record.text); closeMenus(); toast("Copied to clipboard"); }},
      "Copy post text"),
    own ? el("button", {role: "menuitem", type: "button", class: "danger-text", "data-testid": "postDropdownDeleteBtn",
      onclick: function () { closeMenus(); confirmDelete(view); }}, "Delete post") : null);
  item.append(menu);
  button.setAttribute("aria-expanded", "true");
  menu.querySelector("button").focus();
}

function modal(label, ...content) {
  const dialog = el("div", {class: "dialog", role: "dialog", "aria-modal": "true", "aria-label": label}, ...content);
  const backdrop = el("div", {class: "backdrop", onclick: function (event) { if (event.target === backdrop) backdrop.remove(); }}, dialog);
  layerRoot.append(backdrop);
  return backdrop;
}

function confirmDelete(view) {
  const layer = modal("Delete this post?",
    el("h2", {}, "Delete this post?"),
    el("p", {class: "muted"}, "If you remove this post, you won't be able to recover it."),
    el("div", {class: "bar"},
      el("button", {type: "button", "data-testid": "cancelBtn", onclick: function () { layer.remove(); }}, "Cancel"),
      el("button", {type: "button", class: "danger", "data-testid": "confirmBtn", onclick: async function () {
        await callApi(S("com.bluehaze.repo.deleteRecord"), null, {repo: session.did, collection: S("app.bluehaze.feed.post"), rkey: rkeyOf(view.uri)});
        layer.remove();
        toast("Post deleted");
        if (location.pathname === postPath(view)) navigate("/profile/" + session.handle); else render();
      }}, "Delete")));
  layer.querySelector("[data-testid=confirmBtn]").focus();
}

function openComposer(parent) {
  const picked = [];
  const editor = el("textarea", {"aria-label": "Rich-Text Editor", "data-testid": "composerTextInput",
    placeholder: parent ? "Write your reply" : "What's up?", maxlength: "300"});
  const thumbs = el("div", {class: "thumbs"});
  const picker = el("input", {type: "file", accept: "image/png,image/jpeg,image/webp,image/gif", multiple: true,
    class: "visually-hidden", "data-testid": "mediaInput", "aria-label": "Upload image"});
  const counter = el("span", {class: "muted"}, "300");
  const publish = el("button", {type: "button", class: "primary", "data-testid": "composerPublishBtn",
    "aria-label": parent ? "Publish reply" : "Publish post"}, parent ? "Reply" : "Post");

  function drawThumbs() {
    thumbs.replaceChildren(...picked.map(function (entry, index) {
      return el("div", {class: "thumb"},
        el("img", {src: entry.url, alt: entry.alt || ""}),
        el("button", {type: "button", class: "alt-btn", "data-testid": "altTextButton",
          "aria-label": entry.alt ? "Edit alt text" : "Add alt text", onclick: function () { editAlt(entry); }}, "ALT"),
        el("button", {type: "button", class: "remove", "aria-label": "Remove image",
          onclick: function () { picked.splice(index, 1); drawThumbs(); }}, "x"));
    }));
  }

  function editAlt(entry) {
    const altInput = el("textarea", {"aria-label": "Alt text", "data-testid": "altTextImageInput", placeholder: "Describe the image"});
    altInput.value = entry.alt || "";
    const altLayer = modal("Add alt text", el("div", {class: "alt"},
      el("h2", {}, "Add alt text"),
      el("img", {src: entry.url, alt: "", style: "max-width:100%;max-height:200px"}),
      altInput,
      el("div", {class: "bar"}, el("span"),
        el("button", {type: "button", class: "primary", "data-testid": "altTextImageSaveBtn", "aria-label": "Save alt text",
          onclick: function () { entry.alt = altInput.value; altLayer.remove(); drawThumbs(); }}, "Save"))));
    altInput.focus();
  }

  picker.addEventListener("change", function () {
    for (const file of picker.files) if (picked.length < 4) picked.push({file: file, url: URL.createObjectURL(file), alt: ""});
    picker.value = "";
    drawThumbs();
  });
  editor.addEventListener("input", function () { counter.textContent = String(300 - editor.value.length); });
  publish.addEventListener("click", async function () {
    if (!editor.value.trim() && !picked.length) return;
    publish.disabled = true;
    try {
      const record = {$type: S("app.bluehaze.feed.post"), text: editor.value, createdAt: new Date().toISOString()};
      if (picked.length) {
        const embedded = [];
        for (const entry of picked) {
          const uploaded = await callApi(S("com.bluehaze.repo.uploadBlob"), null, entry.file, entry.file.type);
          embedded.push({image: uploaded.blob, alt: entry.alt || ""});
        }
        record.embed = {$type: S("app.bluehaze.embed.images"), images: embedded};
      }
      if (parent) {
        const rootRef = parent.record.reply ? parent.record.reply.root : {uri: parent.uri, cid: parent.cid};
        record.reply = {root: rootRef, parent: {uri: parent.uri, cid: parent.cid}};
      }
      await callApi(S("com.bluehaze.repo.createRecord"), null, {repo: session.did, collection: S("app.bluehaze.feed.post"), record: record});
      layer.remove();
      toast(parent ? "Your reply has been published" : "Your post has been published");
      render();
    } catch (error) {
      publish.disabled = false;
      toast("Failed to post: " + error.message);
    }
  });

  const layer = modal(parent ? "Reply to post" : "Compose new post",
    el("div", {class: "bar"},
      el("button", {type: "button", "data-testid": "composerDiscardButton", "aria-label": "Cancel", onclick: function () { layer.remove(); }}, "Cancel"),
      publish),
    parent ? el("div", {class: "muted", "data-testid": "composerReplyTo"},
      "Replying to " + parent.author.displayName + ": " + parent.record.text.slice(0, 80)) : null,
    editor, thumbs,
    el("div", {class: "toolbar"},
      el("button", {type: "button", class: "icon", "data-testid": "openGalleryBtn", "aria-label": "Gallery",
        onclick: function () { picker.click(); }}, "Add image"),
      picker, counter));
  editor.focus();
}

async function feedView(header, method, params) {
  const list = el("div", {"aria-label": "Feed", "data-testid": "feed"});
  mainColumn.replaceChildren(header, list);
  let cursor = null;
  async function loadMore() {
    const query = Object.assign({limit: "30"}, params);
    if (cursor) query.cursor = cursor;
    const page = await callApi(method, query);
    list.querySelectorAll(".more").forEach(function (button) { button.remove(); });
    for (const entry of page.feed) list.append(postItem(entry.post, {}));
    cursor = page.cursor;
    if (cursor) list.append(el("button", {type: "button", class: "more", onclick: loadMore}, "Load more posts"));
    if (!list.querySelector(".post")) list.append(el("p", {class: "header muted"}, "No posts yet."));
  }
  await loadMore();
}

async function threadView(handle, rkey) {
  const uri = S("at://did:web:") + handle + "/" + S("app.bluehaze.feed.post") + "/" + rkey;
  try {
    const reply = await callApi(S("app.bluehaze.feed.getPostThread"), {uri: uri});
    const thread = reply.thread;
    mainColumn.replaceChildren(el("div", {class: "header"}, el("h1", {}, "Post")),
      thread.parent ? postItem(thread.parent.post, {}) : null,
      postItem(thread.post, {focus: true, parentName: thread.parent && thread.parent.post.author.displayName}),
      ...thread.replies.map(function (child) { return postItem(child.post, {parentName: thread.post.author.displayName}); }));
  } catch (error) {
    mainColumn.replaceChildren(el("div", {class: "header"}, el("h1", {}, "Post not found"), el("p", {class: "muted"}, "The post may have been deleted.")));
  }
}

async function render() {
  closeMenus();
  const parts = decodeURIComponent(location.pathname).split("/").filter(Boolean);
  if (parts[0] === "profile" && parts.length === 4 && parts[2] === "post") return threadView(parts[1], parts[3]);
  if (parts[0] === "profile" && parts.length === 2) {
    try {
      const actor = await callApi(S("app.bluehaze.actor.getProfile"), {actor: parts[1]});
      document.title = actor.displayName + " (@" + actor.handle + ") - Bluehaze";
      return feedView(el("div", {class: "header", "data-testid": "profileHeader"}, el("h1", {}, actor.displayName),
        el("div", {class: "muted"}, "@" + actor.handle + " · " + actor.postsCount + " posts"), el("p", {}, actor.description)),
        S("app.bluehaze.feed.getAuthorFeed"), {actor: actor.handle});
    } catch (error) {
      return mainColumn.replaceChildren(el("div", {class: "header"}, el("h1", {}, "Profile not found")));
    }
  }
  document.title = "Home - Bluehaze";
  return feedView(el("div", {class: "header"}, el("h1", {}, "Following")), S("app.bluehaze.feed.getTimeline"), {});
}

document.getElementById("compose-open").addEventListener("click", function () { openComposer(null); });
document.addEventListener("click", function (event) { if (!event.target.closest(".menu,[data-testid=postDropdownBtn]")) closeMenus(); });
document.addEventListener("keydown", function (event) {
  if (event.key !== "Escape") return;
  closeMenus();
  if (layerRoot.lastElementChild) layerRoot.lastElementChild.remove();
});
window.addEventListener("popstate", render);
callApi(S("com.bluehaze.server.getSession")).then(function (who) {
  session = who;
  const nav = document.getElementById("nav-profile");
  nav.setAttribute("href", "/profile/" + who.handle);
  nav.addEventListener("click", followLink);
  return render();
});

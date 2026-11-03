// Bluehaze web client: renders every view from the JSON API (#153). Fictional site for a benchmark task.
"use strict";

const main = document.getElementById("main");
const layers = document.getElementById("layers");
let session = null;

function el(tag, attrs, ...kids) {
  const node = document.createElement(tag);
  for (const [name, value] of Object.entries(attrs || {})) {
    if (name.startsWith("on")) node.addEventListener(name.slice(2), value);
    else if (value !== null && value !== undefined && value !== false) node.setAttribute(name, value === true ? "" : value);
  }
  for (const kid of kids.flat()) if (kid !== null && kid !== undefined) node.append(kid);
  return node;
}

async function xrpc(method, params, body, contentType) {
  const query = params ? "?" + new URLSearchParams(params) : "";
  const init = body === undefined ? {} : {method: "POST", body: contentType ? body : JSON.stringify(body),
    headers: {"Content-Type": contentType || "application/json"}};
  const reply = await fetch("/xrpc/" + method + query, init);
  const payload = await reply.json();
  if (!reply.ok) throw new Error(payload.message || payload.error || reply.status);
  return payload;
}

function toast(text) {
  const box = document.getElementById("toast");
  box.textContent = text;
  box.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { box.hidden = true; }, 3000);
}

function rkeyOf(uri) { return uri.split("/").pop(); }
function postPath(view) { return "/profile/" + view.author.handle + "/post/" + rkeyOf(view.uri); }
function go(path) { history.pushState(null, "", path); render(); }
function when(iso) { return new Date(iso).toLocaleString("en-US", {month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"}); }

function postItem(view, opts) {
  const own = session && view.author.handle === session.handle;
  const testid = (opts.focus ? "postThreadItem-by-" : "feedItem-by-") + view.author.handle;
  const reply = view.record.reply;
  const images = (view.embed && view.embed.images) || [];
  const item = el("div", {class: "post" + (opts.focus ? " focus" : ""), role: opts.focus ? null : "link",
      "data-testid": testid, "data-post-uri": view.uri, tabindex: opts.focus ? null : "0",
      onclick: (event) => { if (!opts.focus && !event.target.closest("a,button,.menu")) go(postPath(view)); }},
    el("div", {class: "meta"},
      el("a", {href: "/profile/" + view.author.handle, "aria-label": view.author.displayName, onclick: link},
        el("strong", {}, view.author.displayName)), " ",
      el("span", {class: "handle"}, "@" + view.author.handle), " · ",
      el("time", {datetime: view.indexedAt}, el("a", {href: postPath(view), onclick: link,
        "aria-label": view.record.text.slice(0, 40) || "Post", "data-tooltip": view.indexedAt}, when(view.indexedAt)))),
    reply ? el("div", {class: "context"}, "Reply to " + (opts.parentName || "a post")) : null,
    el("div", {class: "text", "data-testid": "postText"}, view.record.text),
    images.length ? el("div", {class: "images"}, images.map((image) => el("img", {src: image.thumb, alt: image.alt}))) : null,
    el("div", {class: "actions"},
      el("button", {class: "icon", type: "button", "data-testid": "replyBtn",
        "aria-label": "Reply (" + view.replyCount + (view.replyCount === 1 ? " reply)" : " replies)"),
        onclick: () => openComposer(view)}, "Reply " + view.replyCount),
      el("button", {class: "icon", type: "button", "data-testid": "postDropdownBtn", "aria-label": "Open post options menu",
        "aria-haspopup": "menu", onclick: (event) => openMenu(item, view, own, event.currentTarget)}, "..."))
  );
  return item;
}

function link(event) { event.preventDefault(); go(event.currentTarget.getAttribute("href")); }

function closeMenus() { document.querySelectorAll(".menu").forEach((menu) => menu.remove()); }

function openMenu(item, view, own, button) {
  closeMenus();
  const menu = el("div", {class: "menu", role: "menu", "aria-label": "Post options"},
    el("button", {role: "menuitem", type: "button", "data-testid": "postDropdownCopyTextBtn",
      onclick: () => { navigator.clipboard && navigator.clipboard.writeText(view.record.text); closeMenus(); toast("Copied to clipboard"); }},
      "Copy post text"),
    own ? el("button", {role: "menuitem", type: "button", class: "danger-text", "data-testid": "postDropdownDeleteBtn",
      onclick: () => { closeMenus(); confirmDelete(view); }}, "Delete post") : null);
  item.append(menu);
  button.setAttribute("aria-expanded", "true");
  menu.querySelector("button").focus();
}

function modal(label, ...content) {
  const dialog = el("div", {class: "dialog", role: "dialog", "aria-modal": "true", "aria-label": label}, ...content);
  const backdrop = el("div", {class: "backdrop", onclick: (event) => { if (event.target === backdrop) backdrop.remove(); }}, dialog);
  layers.append(backdrop);
  return backdrop;
}

function confirmDelete(view) {
  const layer = modal("Delete this post?",
    el("h2", {}, "Delete this post?"),
    el("p", {class: "muted"}, "If you remove this post, you won't be able to recover it."),
    el("div", {class: "bar"},
      el("button", {type: "button", "data-testid": "cancelBtn", onclick: () => layer.remove()}, "Cancel"),
      el("button", {type: "button", class: "danger", "data-testid": "confirmBtn", onclick: async () => {
        await xrpc("com.bluehaze.repo.deleteRecord", null, {repo: session.did, collection: "app.bluehaze.feed.post", rkey: rkeyOf(view.uri)});
        layer.remove();
        toast("Post deleted");
        if (location.pathname === postPath(view)) go("/profile/" + session.handle); else render();
      }}, "Delete")));
  layer.querySelector("[data-testid=confirmBtn]").focus();
}

function openComposer(parent) {
  const files = [];
  const text = el("textarea", {"aria-label": "Rich-Text Editor", "data-testid": "composerTextInput",
    placeholder: parent ? "Write your reply" : "What's up?", maxlength: "300"});
  const thumbs = el("div", {class: "thumbs"});
  const picker = el("input", {type: "file", accept: "image/png,image/jpeg,image/webp,image/gif", multiple: true,
    class: "visually-hidden", "data-testid": "mediaInput", "aria-label": "Upload image"});
  const counter = el("span", {class: "muted"}, "300");
  const publish = el("button", {type: "button", class: "primary", "data-testid": "composerPublishBtn",
    "aria-label": parent ? "Publish reply" : "Publish post"}, parent ? "Reply" : "Post");

  function drawThumbs() {
    thumbs.replaceChildren(...files.map((entry, index) => el("div", {class: "thumb"},
      el("img", {src: entry.url, alt: entry.alt || ""}),
      el("button", {type: "button", class: "alt-btn", "data-testid": "altTextButton",
        "aria-label": entry.alt ? "Edit alt text" : "Add alt text", onclick: () => editAlt(entry)}, "ALT"),
      el("button", {type: "button", class: "remove", "aria-label": "Remove image",
        onclick: () => { files.splice(index, 1); drawThumbs(); }}, "x"))));
  }

  function editAlt(entry) {
    const input = el("textarea", {"aria-label": "Alt text", "data-testid": "altTextImageInput", placeholder: "Describe the image"});
    input.value = entry.alt || "";
    const altLayer = modal("Add alt text", el("div", {class: "alt"},
      el("h2", {}, "Add alt text"),
      el("img", {src: entry.url, alt: "", style: "max-width:100%;max-height:200px"}),
      input,
      el("div", {class: "bar"}, el("span"),
        el("button", {type: "button", class: "primary", "data-testid": "altTextImageSaveBtn", "aria-label": "Save alt text",
          onclick: () => { entry.alt = input.value; altLayer.remove(); drawThumbs(); }}, "Save"))));
    input.focus();
  }

  picker.addEventListener("change", () => {
    for (const file of picker.files) if (files.length < 4) files.push({file, url: URL.createObjectURL(file), alt: ""});
    picker.value = "";
    drawThumbs();
  });
  text.addEventListener("input", () => { counter.textContent = String(300 - text.value.length); });
  publish.addEventListener("click", async () => {
    if (!text.value.trim() && !files.length) return;
    publish.disabled = true;
    try {
      const record = {$type: "app.bluehaze.feed.post", text: text.value, createdAt: new Date().toISOString()};
      if (files.length) {
        const images = [];
        for (const entry of files) {
          const uploaded = await xrpc("com.bluehaze.repo.uploadBlob", null, entry.file, entry.file.type);
          images.push({image: uploaded.blob, alt: entry.alt || ""});
        }
        record.embed = {$type: "app.bluehaze.embed.images", images};
      }
      if (parent) {
        const root = parent.record.reply ? parent.record.reply.root : {uri: parent.uri, cid: parent.cid};
        record.reply = {root, parent: {uri: parent.uri, cid: parent.cid}};
      }
      await xrpc("com.bluehaze.repo.createRecord", null, {repo: session.did, collection: "app.bluehaze.feed.post", record});
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
      el("button", {type: "button", "data-testid": "composerDiscardButton", "aria-label": "Cancel", onclick: () => layer.remove()}, "Cancel"),
      publish),
    parent ? el("div", {class: "muted", "data-testid": "composerReplyTo"},
      "Replying to " + parent.author.displayName + ": " + parent.record.text.slice(0, 80)) : null,
    text, thumbs,
    el("div", {class: "toolbar"},
      el("button", {type: "button", class: "icon", "data-testid": "openGalleryBtn", "aria-label": "Gallery",
        onclick: () => picker.click()}, "Add image"),
      picker, counter));
  text.focus();
}

async function feedView(header, method, params) {
  const list = el("div", {"aria-label": "Feed", "data-testid": "feed"});
  main.replaceChildren(header, list);
  let cursor;
  async function more() {
    const page = await xrpc(method, Object.assign({limit: "30"}, params, cursor ? {cursor} : {}));
    list.querySelectorAll(".more").forEach((button) => button.remove());
    for (const entry of page.feed) list.append(postItem(entry.post, {}));
    cursor = page.cursor;
    if (cursor) list.append(el("button", {type: "button", class: "more", onclick: more}, "Load more posts"));
    if (!list.querySelector(".post")) list.append(el("p", {class: "header muted"}, "No posts yet."));
  }
  await more();
}

async function threadView(handle, rkey) {
  const uri = "at://did:web:" + handle + "/app.bluehaze.feed.post/" + rkey;
  try {
    const {thread} = await xrpc("app.bluehaze.feed.getPostThread", {uri});
    main.replaceChildren(el("div", {class: "header"}, el("h1", {}, "Post")),
      thread.parent ? postItem(thread.parent.post, {}) : null,
      postItem(thread.post, {focus: true, parentName: thread.parent && thread.parent.post.author.displayName}),
      ...thread.replies.map((child) => postItem(child.post, {parentName: thread.post.author.displayName})));
  } catch (error) {
    main.replaceChildren(el("div", {class: "header"}, el("h1", {}, "Post not found"), el("p", {class: "muted"}, "The post may have been deleted.")));
  }
}

async function render() {
  closeMenus();
  const path = decodeURIComponent(location.pathname);
  const thread = path.match(/^\/profile\/([^/]+)\/post\/([^/]+)\/?$/);
  const profile = path.match(/^\/profile\/([^/]+)\/?$/);
  if (thread) return threadView(thread[1], thread[2]);
  if (profile) {
    try {
      const actor = await xrpc("app.bluehaze.actor.getProfile", {actor: profile[1]});
      document.title = actor.displayName + " (@" + actor.handle + ") - Bluehaze";
      return feedView(el("div", {class: "header", "data-testid": "profileHeader"}, el("h1", {}, actor.displayName),
        el("div", {class: "muted"}, "@" + actor.handle + " · " + actor.postsCount + " posts"), el("p", {}, actor.description)),
        "app.bluehaze.feed.getAuthorFeed", {actor: actor.handle});
    } catch (error) {
      return main.replaceChildren(el("div", {class: "header"}, el("h1", {}, "Profile not found")));
    }
  }
  document.title = "Home - Bluehaze";
  return feedView(el("div", {class: "header"}, el("h1", {}, "Following")), "app.bluehaze.feed.getTimeline", {});
}

document.getElementById("compose-open").addEventListener("click", () => openComposer(null));
document.addEventListener("click", (event) => { if (!event.target.closest(".menu,[data-testid=postDropdownBtn]")) closeMenus(); });
document.addEventListener("keydown", (event) => { if (event.key === "Escape") { closeMenus(); const top = layers.lastElementChild; if (top) top.remove(); } });
window.addEventListener("popstate", render);
xrpc("com.bluehaze.server.getSession").then((who) => {
  session = who;
  const nav = document.getElementById("nav-profile");
  nav.setAttribute("href", "/profile/" + who.handle);
  nav.addEventListener("click", link);
  return render();
});

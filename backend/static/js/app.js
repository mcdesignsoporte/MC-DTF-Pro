const fileBox = document.getElementById("fileBox");
const imageInput = document.getElementById("imageInput");
const fileText = document.getElementById("fileText");
const previewWrap = document.getElementById("previewWrap");
const previewImg = document.getElementById("previewImg");
const form = document.getElementById("dtfForm");
const processBtn = document.getElementById("processBtn");

const alphaCut = document.getElementById("alphaCut");
const despeckleArea = document.getElementById("despeckleArea");
const edgeContract = document.getElementById("edgeContract");
const upscale = document.getElementById("upscale");

fileBox.addEventListener("click", () => imageInput.click());

imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (!file) return;

  fileText.textContent = file.name;
  const reader = new FileReader();
  reader.onload = e => {
    previewImg.src = e.target.result;
    previewWrap.classList.remove("hidden");
  };
  reader.readAsDataURL(file);
});

fileBox.addEventListener("dragover", e => {
  e.preventDefault();
  fileBox.classList.add("drag");
});

fileBox.addEventListener("dragleave", () => fileBox.classList.remove("drag"));

fileBox.addEventListener("drop", e => {
  e.preventDefault();
  fileBox.classList.remove("drag");
  if (e.dataTransfer.files.length > 0) {
    imageInput.files = e.dataTransfer.files;
    imageInput.dispatchEvent(new Event("change"));
  }
});

document.querySelectorAll("[data-preset]").forEach(btn => {
  btn.addEventListener("click", () => {
    const preset = btn.dataset.preset;

    if (preset === "soft") {
      alphaCut.value = 60;
      despeckleArea.value = 2;
      edgeContract.value = 0;
      upscale.value = 1;
    }

    if (preset === "normal") {
      alphaCut.value = 80;
      despeckleArea.value = 3;
      edgeContract.value = 0;
      upscale.value = 1;
    }

    if (preset === "strong") {
      alphaCut.value = 140;
      despeckleArea.value = 12;
      edgeContract.value = 1;
      upscale.value = 1;
    }
  });
});

form.addEventListener("submit", () => {
  processBtn.textContent = "Procesando...";
  processBtn.disabled = true;
});

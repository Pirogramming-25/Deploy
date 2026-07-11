// CSRF 토큰 (meta 태그에서 읽기)
function getCsrfToken() {
  const el = document.querySelector('meta[name="csrf-token"]');
  return el ? el.getAttribute("content") : "";
}

// 공통 POST 헬퍼
async function postForm(url, data = {}) {
  const body = new URLSearchParams(data);
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCsrfToken(),
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });
  return res;
}

// 이벤트 위임 (AJAX 로 DOM 이 바뀌어도 동작)
document.addEventListener("click", async (e) => {
  // 찜하기 토글
  const starBtn = e.target.closest(".star-btn");
  if (starBtn) {
    e.preventDefault();
    const res = await postForm(starBtn.dataset.starUrl);
    if (res.status === 401) {
      const data = await res.json();
      alert("로그인이 필요합니다.");
      window.location.href = data.login_url || "/accounts/login/";
      return;
    }
    const data = await res.json();
    starBtn.classList.toggle("on", data.starred);
    starBtn.classList.remove("pop");
    void starBtn.offsetWidth;
    starBtn.classList.add("pop");
    const countEl = starBtn.querySelector(".star-count");
    if (countEl) countEl.textContent = data.count;
    return;
  }

  // 관심도 +/-
  const interestBtn = e.target.closest(".interest-btn");
  if (interestBtn) {
    e.preventDefault();
    const box = interestBtn.closest(".interest");
    const res = await postForm(box.dataset.interestUrl, { action: interestBtn.dataset.action });
    const data = await res.json();
    box.querySelector(".interest-value").textContent = data.interest;
    return;
  }

  // 페이지네이션
  const pageBtn = e.target.closest(".page-btn");
  if (pageBtn) {
    e.preventDefault();
    loadIdeas(pageBtn.dataset.page);
    return;
  }
});

// AJAX 검색 / 정렬 / 페이지 이동
const container = document.getElementById("idea-container");
const searchInput = document.getElementById("search-input");
const sortSelect = document.getElementById("sort-select");

async function loadIdeas(page = 1) {
  if (!container) return;
  const params = new URLSearchParams();
  if (searchInput && searchInput.value.trim()) params.set("q", searchInput.value.trim());
  if (sortSelect) params.set("sort", sortSelect.value);
  params.set("page", page);

  const res = await fetch(`/?${params.toString()}`, {
    headers: { "X-Requested-With": "XMLHttpRequest" },
  });
  container.innerHTML = await res.text();
  history.replaceState(null, "", `/?${params.toString()}`);
}

if (sortSelect) sortSelect.addEventListener("change", () => loadIdeas(1));

if (searchInput) {
  let timer;
  searchInput.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => loadIdeas(1), 300);
  });
}

const API = "";
let dashboard = null;
let currentSubject = null;
let currentLessons = [];
let currentLesson = null;
let selectedQuickAnswer = null;
let currentQuizSubject = null;
let currentQuiz = [];
let quizAnswers = [];

const subjectIcons = {
  python: "🐍",
  math: "🧮",
  english: "📖",
  datascience: "📊"
};

async function api(path, options = {}) {
  const response = await fetch(API + path, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));
}

function goTo(page) {
  document.querySelectorAll(".page").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(".nav-link").forEach(el => el.classList.remove("active"));
  const section = document.getElementById("page-" + page);
  if (section) section.classList.add("active");
  const nav = document.querySelector(`.nav-link[data-page="${page}"]`);
  if (nav) nav.classList.add("active");

  if (page === "home") loadDashboard();
  if (page === "learn") renderLearnSubjects();
  if (page === "quizzes") renderQuizSubjects();
  if (page === "results") loadResults();
  if (page === "calendar") renderCalendar();
  if (page === "badges") renderBadges();
  if (page === "profile") loadProfile();
  if (page === "buddy") document.getElementById("chat-input").focus();
}

document.querySelectorAll("[data-page]").forEach(button => {
  button.addEventListener("click", () => goTo(button.dataset.page));
});
document.querySelectorAll("[data-go]").forEach(button => {
  button.addEventListener("click", () => goTo(button.dataset.go));
});
document.querySelectorAll("[data-open-subject]").forEach(button => {
  button.addEventListener("click", async () => {
    goTo("learn");
    await openSubject(button.dataset.openSubject);
  });
});

function greetingText(name) {
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  return `${greeting}, ${name}! ${hour < 12 ? "☀️" : hour < 17 ? "🌷" : "🌙"}`;
}

async function loadDashboard() {
  try {
    dashboard = await api("/api/dashboard");
    renderDashboard();
  } catch (error) {
    console.error(error);
  }
}

function renderDashboard() {
  if (!dashboard) return;
  const d = dashboard;
  const name = d.profile.name || "Learner";
  document.getElementById("greeting").textContent = greetingText(name);
  document.getElementById("top-name").textContent = name;
  document.getElementById("top-level").textContent = d.profile.level;
  document.getElementById("top-avatar").textContent = name.charAt(0).toUpperCase();
  document.getElementById("top-streak").textContent = d.streak;
  document.getElementById("stat-lessons").textContent = d.completed;
  document.getElementById("stat-total").textContent = `of ${d.total_lessons} lessons`;
  document.getElementById("stat-streak").textContent = d.streak;
  document.getElementById("stat-quizzes").textContent = d.quiz_attempts;
  document.getElementById("stat-progress").textContent = d.progress + "%";
  document.getElementById("overall-bar").style.width = d.progress + "%";

  document.getElementById("goal-text").textContent =
    `Complete ${d.goal} ${d.goal === 1 ? "lesson" : "lessons"} today`;
  document.getElementById("goal-count").textContent = `${d.today_completed} / ${d.goal}`;
  document.getElementById("goal-percent").textContent = d.goal_percent + "%";
  document.getElementById("goal-bar").style.width = d.goal_percent + "%";
  document.getElementById("goal-cheer").textContent = d.goal_reached
    ? "🎉 Goal reached! You showed up for yourself today!"
    : "🌷 A little progress goes a long way. Keep going!";

  renderWeek(d.week, "week-days");
  renderHomeSubjects(d.subjects);
}

function renderHomeSubjects(subjects) {
  const container = document.getElementById("home-subjects");
  container.innerHTML = subjects.map(subject => {
    const icon = subjectIcons[subject.id] || "📘";
    const color = subject.id === "math" ? "orange" :
      subject.id === "english" ? "purple" :
      subject.id === "datascience" ? "green" : "pink";
    const percent = subject.total ? Math.round(subject.completed / subject.total * 100) : 0;
    return `
      <article class="subject-card ${color}">
        <div class="subject-emoji">${icon}</div>
        <h3>${escapeHTML(subject.name)}</h3>
        <div class="subject-meta">${subject.total} lessons • ${percent}% complete</div>
        <p>${escapeHTML(subject.description)}</p>
        <button class="primary-btn" data-subject-open="${subject.id}">Start Learning →</button>
      </article>`;
  }).join("");
  container.querySelectorAll("[data-subject-open]").forEach(button => {
    button.addEventListener("click", async () => {
      goTo("learn");
      await openSubject(button.dataset.subjectOpen);
    });
  });
}

function renderLearnSubjects() {
  if (!dashboard) return;
  const container = document.getElementById("learn-subjects");
  container.innerHTML = dashboard.subjects.map(subject => {
    const color = subject.id === "math" ? "orange" :
      subject.id === "english" ? "purple" :
      subject.id === "datascience" ? "green" : "pink";
    const percent = subject.total ? Math.round(subject.completed / subject.total * 100) : 0;
    return `
      <article class="subject-card ${color}">
        <div class="subject-emoji">${subjectIcons[subject.id] || "📘"}</div>
        <h3>${escapeHTML(subject.name)}</h3>
        <div class="subject-meta">${subject.completed}/${subject.total} lessons • ${percent}%</div>
        <p>${escapeHTML(subject.description)}</p>
        <button class="primary-btn" data-subject-open="${subject.id}">Explore Lessons →</button>
      </article>`;
  }).join("");
  container.querySelectorAll("[data-subject-open]").forEach(button => {
    button.addEventListener("click", () => openSubject(button.dataset.subjectOpen));
  });
}

async function openSubject(subjectId) {
  currentSubject = subjectId;
  currentLesson = null;
  const area = document.getElementById("lesson-area");
  area.innerHTML = `<div class="empty-state"><div>🌷</div><h3>Loading lessons...</h3></div>`;
  try {
    const data = await api(`/api/lessons/${subjectId}`);
    currentLessons = data.lessons;
    renderLessonList(data.subject);
  } catch (error) {
    area.innerHTML = `<div class="empty-state"><h3>Oops!</h3><p>${escapeHTML(error.message)}</p></div>`;
  }
}

function renderLessonList(subject) {
  const area = document.getElementById("lesson-area");
  const list = currentLessons.map((lesson, index) => `
    <button class="lesson-item ${currentLesson?.id === lesson.id ? "selected" : ""}" data-lesson-index="${index}">
      <span>
        <strong>${index + 1}. ${escapeHTML(lesson.title)}</strong>
        <small>${escapeHTML(lesson.difficulty)} • ${lesson.duration} min</small>
      </span>
      <span class="lesson-status">${lesson.completed ? "✓ Done" : "Start →"}</span>
    </button>`).join("");
  area.innerHTML = `
    <div class="section-heading"><div><h2>${escapeHTML(subject.name)} lessons</h2><p>${currentLessons.filter(x => x.completed).length} of ${currentLessons.length} completed</p></div></div>
    <div class="lesson-list">${list}</div>
    <div id="lesson-detail">
      <div class="empty-state"><div>🐣</div><h3>Choose a lesson</h3><p>Peep believes in you!</p></div>
    </div>`;
  area.querySelectorAll("[data-lesson-index]").forEach(button => {
    button.addEventListener("click", () => {
      const lesson = currentLessons[Number(button.dataset.lessonIndex)];
      currentLesson = lesson;
      selectedQuickAnswer = null;
      renderLessonList(subject);
      renderLesson(lesson);
    });
  });
}

function renderLesson(lesson) {
  const detail = document.getElementById("lesson-detail");
  detail.innerHTML = `
    <article class="lesson-detail">
      <span class="tag">${escapeHTML(currentSubject.toUpperCase())} • ${escapeHTML(lesson.difficulty)}</span>
      <h2>${escapeHTML(lesson.title)}</h2>
      <p>${escapeHTML(lesson.content)}</p>
      <h3>💡 Example</h3>
      <pre class="lesson-example">${escapeHTML(lesson.example)}</pre>
      <div class="tip-box">🌟 <strong>Peep's tip:</strong> ${escapeHTML(lesson.tip)}</div>
      <div class="quick-check">
        <h3>✨ Quick Check</h3>
        <p><strong>${escapeHTML(lesson.question)}</strong></p>
        <div class="answer-options" id="quick-options">
          ${lesson.options.map((option, i) => `
            <button class="answer-option" data-answer="${i}">${String.fromCharCode(65 + i)}. ${escapeHTML(option)}</button>
          `).join("")}
        </div>
        <div class="feedback" id="quick-feedback"></div>
        <button class="secondary-btn" id="check-answer">Check Answer</button>
      </div>
      <div class="lesson-actions">
        <button class="primary-btn" id="complete-lesson">${lesson.completed ? "✓ Completed" : "Mark Lesson Complete 💗"}</button>
        <button class="secondary-btn" id="next-lesson">Next Lesson →</button>
      </div>
    </article>`;

  document.querySelectorAll("[data-answer]").forEach(button => {
    button.addEventListener("click", () => {
      selectedQuickAnswer = Number(button.dataset.answer);
      document.querySelectorAll("[data-answer]").forEach(x => x.classList.remove("chosen"));
      button.classList.add("chosen");
    });
  });
  document.getElementById("check-answer").addEventListener("click", checkQuickAnswer);
  document.getElementById("complete-lesson").addEventListener("click", markComplete);
  document.getElementById("next-lesson").addEventListener("click", nextLesson);
}

async function checkQuickAnswer() {
  const feedback = document.getElementById("quick-feedback");
  if (selectedQuickAnswer === null) {
    feedback.textContent = "Choose an answer first 🌷";
    return;
  }
  try {
    const result = await api(`/api/quick-check/${currentLesson.id}`, {
      method: "POST",
      body: JSON.stringify({ answer: selectedQuickAnswer })
    });
    const buttons = document.querySelectorAll("[data-answer]");
    buttons.forEach((button, i) => {
      button.classList.remove("chosen");
      if (i === result.correct_index) button.classList.add("correct");
      else if (i === selectedQuickAnswer) button.classList.add("wrong");
    });
    feedback.textContent = `${result.correct ? "🎉 That's right!" : "💡 Not quite."} ${result.explanation}`;
  } catch (error) {
    feedback.textContent = error.message;
  }
}

async function markComplete() {
  if (!currentLesson) return;
  try {
    await api(`/api/lessons/${currentLesson.id}/complete`, {
      method: "POST",
      body: JSON.stringify({})
    });
    await loadDashboard();
    const data = await api(`/api/lessons/${currentSubject}`);
    currentLessons = data.lessons;
    const subject = data.subject;
    currentLesson = currentLessons.find(x => x.id === currentLesson.id);
    renderLessonList(subject);
    renderLesson(currentLesson);
  } catch (error) {
    alert(error.message);
  }
}

function nextLesson() {
  if (!currentLesson) return;
  const index = currentLessons.findIndex(x => x.id === currentLesson.id);
  const next = currentLessons[index + 1];
  if (!next) {
    alert("You reached the end of this subject's lessons! Amazing work! 🌈");
    return;
  }
  currentLesson = next;
  selectedQuickAnswer = null;
  const subject = dashboard.subjects.find(s => s.id === currentSubject);
  renderLessonList({ name: subject?.name || currentSubject });
  renderLesson(next);
}

function renderWeek(week, targetId) {
  const container = document.getElementById(targetId);
  if (!container) return;
  container.innerHTML = week.map(day => `
    <div class="week-day ${day.studied ? "studied" : ""} ${day.today ? "today" : ""}">
      <span>${day.label}</span>
      <strong>${day.number}</strong>
      <div class="day-dot">${day.studied ? "✓" : day.today ? "•" : "×"}</div>
    </div>`).join("");
}

function renderCalendar() {
  if (!dashboard) return;
  const container = document.getElementById("calendar-days");
  container.innerHTML = dashboard.week.map(day => `
    <div class="calendar-cell ${day.studied ? "studied" : ""} ${day.today ? "today" : ""}">
      <strong>${day.label}</strong>
      <span>${day.date}</span>
      <b>${day.studied ? "🌱" : "·"}</b>
    </div>`).join("");
}

function renderBadges() {
  if (!dashboard) return;
  document.getElementById("badges-grid").innerHTML = dashboard.badges.map(badge => `
    <div class="badge-card ${badge.unlocked ? "" : "locked"}">
      <div class="badge-icon">${badge.icon}</div>
      <h3>${escapeHTML(badge.name)}</h3>
      <p>${escapeHTML(badge.description)}</p>
      <span class="badge-state">${badge.unlocked ? "✓ Unlocked" : "🔒 Locked"}</span>
    </div>`).join("");
}

document.getElementById("edit-goal").addEventListener("click", async () => {
  const value = prompt("How many lessons would you like as your daily goal? Choose 1–10:", dashboard?.goal || 1);
  if (value === null) return;
  const target = Number(value);
  if (!Number.isInteger(target) || target < 1 || target > 10) {
    alert("Please enter a whole number from 1 to 10.");
    return;
  }
  try {
    await api("/api/goal", { method: "POST", body: JSON.stringify({ target }) });
    await loadDashboard();
  } catch (error) {
    alert(error.message);
  }
});

function renderQuizSubjects() {
  if (!dashboard) return;
  document.getElementById("quiz-subjects").innerHTML = dashboard.subjects.map(subject => `
    <button class="quiz-subject-btn ${currentQuizSubject === subject.id ? "active" : ""}" data-quiz="${subject.id}">
      ${subjectIcons[subject.id]} ${escapeHTML(subject.name)}
    </button>`).join("");
  document.querySelectorAll("[data-quiz]").forEach(button => {
    button.addEventListener("click", () => startQuiz(button.dataset.quiz));
  });
}

async function startQuiz(subjectId) {
  currentQuizSubject = subjectId;
  quizAnswers = [];
  renderQuizSubjects();
  const area = document.getElementById("quiz-area");
  area.innerHTML = `<div class="empty-state"><div>🧠</div><h3>Loading quiz...</h3></div>`;
  try {
    const data = await api(`/api/quiz/${subjectId}`);
    currentQuiz = data.questions;
    quizAnswers = currentQuiz.map(() => null);
    renderQuiz(data.subject);
  } catch (error) {
    area.textContent = error.message;
  }
}

function renderQuiz(subjectName) {
  const area = document.getElementById("quiz-area");
  area.innerHTML = `
    <div class="section-heading"><div><h2>${escapeHTML(subjectName)} Quiz</h2><p>Choose one answer for each question.</p></div></div>
    <div id="quiz-questions">
      ${currentQuiz.map((q, qi) => `
        <div class="quiz-question">
          <h3>${qi + 1}. ${escapeHTML(q.question)}</h3>
          <div class="quiz-options">
            ${q.options.map((option, oi) => `
              <button class="quiz-option" data-q="${qi}" data-o="${oi}">
                ${String.fromCharCode(65 + oi)}. ${escapeHTML(option)}
              </button>`).join("")}
          </div>
        </div>`).join("")}
    </div>
    <button class="primary-btn" id="submit-quiz">Submit Quiz ✨</button>
    <div id="quiz-result"></div>`;
  document.querySelectorAll("[data-q]").forEach(button => {
    button.addEventListener("click", () => {
      const q = Number(button.dataset.q);
      const o = Number(button.dataset.o);
      quizAnswers[q] = o;
      document.querySelectorAll(`[data-q="${q}"]`).forEach(x => x.classList.remove("selected"));
      button.classList.add("selected");
    });
  });
  document.getElementById("submit-quiz").addEventListener("click", submitQuiz);
}

async function submitQuiz() {
  if (quizAnswers.some(answer => answer === null)) {
    alert("Answer every question before submitting. You can do it! 🌷");
    return;
  }
  try {
    const result = await api(`/api/quiz/${currentQuizSubject}/submit`, {
      method: "POST",
      body: JSON.stringify({ answers: quizAnswers })
    });
    const area = document.getElementById("quiz-result");
    area.innerHTML = `
      <div class="quiz-review">
        <h2>${result.score} / ${result.total} — ${escapeHTML(result.message)}</h2>
        <p>Review your answers below. Learning from mistakes is part of the process.</p>
      </div>
      ${result.review.map((item, i) => `
        <div class="quiz-review">
          <strong>${i + 1}. ${escapeHTML(item.question)}</strong><br>
          <span>${item.correct ? "✅ Correct" : "💡 Correct answer: " + escapeHTML(item.options[item.correct_index])}</span>
          <p>${escapeHTML(item.explanation)}</p>
        </div>`).join("")}
      <button class="primary-btn" id="retry-quiz">Try Again ↻</button>`;
    document.getElementById("retry-quiz").addEventListener("click", () => startQuiz(currentQuizSubject));
    document.getElementById("submit-quiz").disabled = true;
    document.querySelectorAll(".quiz-option").forEach(button => {
      const q = Number(button.dataset.q);
      const o = Number(button.dataset.o);
      const answer = result.review[q];
      if (o === answer.correct_index) button.classList.add("correct");
      else if (o === answer.selected && !answer.correct) button.classList.add("wrong");
      button.disabled = true;
    });
    await loadDashboard();
  } catch (error) {
    alert(error.message);
  }
}

async function loadResults() {
  const container = document.getElementById("results-content");
  try {
    const rows = await api("/api/results");
    if (!rows.length) {
      container.innerHTML = `<div class="empty-state"><div>🌱</div><h3>Your results will appear here</h3><p>Complete a quiz to see your first result!</p></div>`;
      return;
    }
    container.innerHTML = `
      <div class="quiz-area">
        <h2>Recent Quiz Attempts</h2>
        ${rows.map(row => `
          <div class="lesson-item">
            <span><strong>${escapeHTML(row.subject)}</strong><small>${new Date(row.attempted_at).toLocaleString()}</small></span>
            <span class="lesson-status">${row.score} / ${row.total}</span>
          </div>`).join("")}
      </div>`;
  } catch (error) {
    container.textContent = error.message;
  }
}

async function loadProfile() {
  try {
    const profile = await api("/api/profile");
    document.getElementById("profile-name").value = profile.name || "";
    document.getElementById("profile-level").value = profile.level || "Beginner";
    document.getElementById("profile-focus").value = profile.focus || "";
  } catch (error) {
    console.error(error);
  }
}

document.getElementById("profile-form").addEventListener("submit", async event => {
  event.preventDefault();
  const name = document.getElementById("profile-name").value.trim();
  const level = document.getElementById("profile-level").value;
  const focus = document.getElementById("profile-focus").value.trim();
  try {
    await api("/api/profile", {
      method: "POST",
      body: JSON.stringify({ name, level, focus })
    });
    document.getElementById("profile-message").textContent = "Profile saved! 💗";
    await loadDashboard();
  } catch (error) {
    document.getElementById("profile-message").textContent = error.message;
  }
});

function addChatMessage(text, who) {
  const windowEl = document.getElementById("chat-window");
  const message = document.createElement("div");
  message.className = `chat-message ${who === "user" ? "user-message" : "peep-message"}`;
  message.textContent = text;
  windowEl.appendChild(message);
  windowEl.scrollTop = windowEl.scrollHeight;
}

async function sendChat(text) {
  const message = text.trim();
  if (!message) return;
  addChatMessage(message, "user");
  try {
    const result = await api("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message })
    });
    addChatMessage(result.reply, "peep");
  } catch (error) {
    addChatMessage("Oops, I couldn't connect just now. Try again in a moment.", "peep");
  }
}

document.getElementById("chat-form").addEventListener("submit", event => {
  event.preventDefault();
  const input = document.getElementById("chat-input");
  const text = input.value;
  input.value = "";
  sendChat(text);
});

document.querySelectorAll("[data-prompt]").forEach(button => {
  button.addEventListener("click", () => sendChat(button.dataset.prompt));
});

async function init() {
  await loadDashboard();
  renderLearnSubjects();
  renderQuizSubjects();
}
init();
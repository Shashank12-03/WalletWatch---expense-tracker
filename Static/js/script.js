const body = document.querySelector("body");
const darkLight = document.querySelector("#darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");
sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));

sidebarClose.addEventListener("click", () => {
  sidebar.classList.add("close", "hoverable");
});
sidebarExpand.addEventListener("click", () => {
  sidebar.classList.remove("close", "hoverable");
});

sidebar.addEventListener("mouseenter", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.remove("close");
  }
});
sidebar.addEventListener("mouseleave", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.add("close");
  }
});

// darkLight.addEventListener("click", () => {
//   body.classList.toggle("dark");
//   if (body.classList.contains("dark")) {
//     document.setI
//     darkLight.classList.replace("bx-sun", "bx-moon");
//   } else {
//     darkLight.classList.replace("bx-moon", "bx-sun");
//   }
// });
const setTheme = (isDark) => {
  if (isDark) {
    body.classList.add("dark");
    darkLight.classList.replace("bx-sun", "bx-moon");
  } else {
    body.classList.remove("dark");
    darkLight.classList.replace("bx-moon", "bx-sun");
  }
};

// Check if user preference is stored in localStorage
const isDarkMode = localStorage.getItem("darkMode") === "true";

// Set initial theme based on user preference
setTheme(isDarkMode);

darkLight.addEventListener("click", () => {
  body.classList.toggle("dark");

  // Update localStorage with the user's preference
  localStorage.setItem("darkMode", body.classList.contains("dark"));

  if (body.classList.contains("dark")) {
    darkLight.classList.replace("bx-sun", "bx-moon");
  } else {
    darkLight.classList.replace("bx-moon", "bx-sun");
  }
});

submenuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    item.classList.toggle("show_submenu");
    submenuItems.forEach((item2, index2) => {
      if (index !== index2) {
        item2.classList.remove("show_submenu");
      }
    });
  });
});

if (window.innerWidth < 768) {
  sidebar.classList.add("close");
} else {
  sidebar.classList.remove("close");
}
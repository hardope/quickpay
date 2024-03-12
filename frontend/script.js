const formOpenBtn = document.querySelector("#form-open"),
  home = document.querySelector(".home"),
  formContainer = document.querySelector(".form_container"),
  formCloseBtn = document.querySelector(".form_close"),
  signupBtn = document.querySelector("#signup"),
  loginBtn = document.querySelector("#login"),
  pwShowHide = document.querySelectorAll(".pw_hide");

formOpenBtn.addEventListener("click", () => home.classList.add("show"));
formCloseBtn.addEventListener("click", () => home.classList.remove("show"));

pwShowHide.forEach((icon) => {
  icon.addEventListener("click", () => {
    let getPwInput = icon.parentElement.querySelector("input");
    if (getPwInput.type === "password") {
      getPwInput.type = "text";
      icon.classList.replace("uil-eye-slash", "uil-eye");
    } else {
      getPwInput.type = "password";
      icon.classList.replace("uil-eye", "uil-eye-slash");
    }
  });
});

signupBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.add("active");
});
loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  formContainer.classList.remove("active");
});

function login() {
  const login_username = document.getElementById("login_username").value;
  const login_password = document.getElementById("login_password").value;

  host = "http://localhost:8000";

  fetch(host + "/account/auth", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: login_username,
      password: login_password,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["status"] === true) {
        localStorage.setItem("quickpay-token", data['jwt']['access']['token']);
        window.location.href = "dashboard.html";
      } else {
        alert("Invalid username or password");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function signup() {
  const signup_username = document.getElementById("signup_username").value;
  const signup_email = document.getElementById("signup_email").value;
  const signup_password = document.getElementById("signup_password").value;
  const signup_confirm_password = document.getElementById("signup_confirm_password").value;

  if (signup_password !== signup_confirm_password) {
    alert("Passwords do not match");
    return;
  }

  host = "http://localhost:8000";

  fetch(host + "/account/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: signup_username,
      email: signup_email,
      password: signup_password,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data["status"] === true) {
        home.classList.remove("show")
        alert("Account created successfully");
      } else {
        alert(data['errors'][0]);
      }
    })
    .catch((error) => {
      alert('An error occured')
      console.error("Error:", error);
    });

    home.classList.add("show");
}
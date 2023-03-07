const users = document.querySelectorAll(".userContainer");
console.log(users);

for (let user of users) {
  const records = user.querySelector(".userRecords");
  const button = user.querySelector("#toggleRecords");
  button.addEventListener("click", (e) => {
    e.preventDefault();
    toggleRecordContainers(records);
  });
}

function toggleRecordContainers(recordContainer) {
  recordContainer.classList.toggle("hiddenValue");
}

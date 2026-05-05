document.addEventListener("DOMContentLoaded", function () {

  const editButtons = document.querySelectorAll(".btn-edit");
  const deleteButtons = document.querySelectorAll(".btn-delete");
  const commentText = document.getElementById("id_body");
  const commentForm = document.getElementById("commentForm");
  const submitButton = document.getElementById("submitButton");

  const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  const deleteConfirm = document.getElementById("deleteConfirm");

  for (let button of editButtons) {
    button.addEventListener("click", (e) => {

      let commentId = e.target.dataset.comment_id;
      let commentContent =
        document.getElementById(`comment${commentId}`).innerText;

      commentText.value = commentContent;
      submitButton.innerText = "Update";

      commentText.classList.add("force-focus");

commentText.focus();
commentText.scrollIntoView({ behavior: "smooth", block: "center" });

setTimeout(() => {
  commentText.classList.remove("force-focus");
}, 800);

      commentForm.action =
        `${window.location.pathname}edit_comment/${commentId}/`;

        
    });
  }

  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {

      let commentId = e.target.dataset.comment_id;

      deleteConfirm.href =
        `${window.location.pathname}delete_comment/${commentId}/`;

      deleteModal.show();
    });
  }

});

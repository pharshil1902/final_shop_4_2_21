function myFunction() {
    // Get the checkbox
    var checkBox = document.getElementsById("add");
    // Get the output text
    var text = document.getElementById("hello");
    
  
    // If the checkbox is checked, display the output text
    if (checkBox.checked == true){
      text.style.display = "block";
    } else {
      text.style.display = "none";
    }
  }
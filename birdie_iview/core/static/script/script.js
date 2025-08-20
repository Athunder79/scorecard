addEventListener('DOMContentLoaded', function () {

  let location = document.getElementById("location");
  let map = document.getElementById("show-map");
  let nextHole = document.getElementById("next-hole");
  let currentHole = document.getElementById("current-hole");
  let atMyBall = document.getElementById("at-my-ball");
  let courseFinders = document.getElementsByClassName("course-finder");

  // Check if the element exists before adding the event listener
  if (location != null){ location.addEventListener("click", getLocation); }
  if (map != null){ map.addEventListener("click", showMap); }
  if (nextHole != null){ nextHole.addEventListener("click", updateShotEndPosition); }
  if (currentHole != null){ colourCells(); }
  if (atMyBall != null){ atMyBall.addEventListener("click", updateShotEndShotPosition); }
  for (let courseFinder of courseFinders) { courseFinder.addEventListener("click", getCourseLocation); }

  let roundHeadings = document.querySelectorAll('h3.round-heading');

  // Toggle hide class on round headings
  roundHeadings.forEach(heading => {
    heading.addEventListener('click', function () {
      let roundDetails = heading.nextElementSibling;
      roundDetails.classList.toggle('hide');
    });
  });

  // ---- Toggle Miss Type checkboxes ----
  let missTypeHeading = document.querySelector(".toggle-miss-type");
  if (missTypeHeading) {
    missTypeHeading.addEventListener("click", function() {
      let options = document.querySelector(".miss-type-options");
      let fieldset = document.querySelector(".miss-type");
      if (options) {
        if (options.classList.contains("d-none")) {
          options.style.display = "flex"; // show
          options.style.opacity = 0;
          setTimeout(() => { options.style.opacity = 1; }, 10);
        } else {
          options.style.opacity = 0;
          setTimeout(() => { options.style.display = "none"; }, 200);
        }
        options.classList.toggle("d-none");
        fieldset.classList.toggle("open"); // rotate arrow
      }
    });
  }
});

// ---- Get user location for course finder ----
function getCourseLocation(){
  console.log("getUserLocation function called");
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;
      console.log("Latitude: " + latitude + " Longitude: " + longitude);
      window.location.href = "/find-golf-courses/" + latitude + "/" + longitude;
    });
  }
}

// ---- Get the latitude and longitude from browser for shot form ----
function getLocation() {
  if (navigator.geolocation){
    const options = {enableHighAccuracy: true};
    navigator.geolocation.getCurrentPosition(showPosition, showError, options);
  } else {
    result.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function updateShotEndPosition(){
  if (navigator.geolocation){
    const options = {enableHighAccuracy: true};
    navigator.geolocation.getCurrentPosition(showEndPosition, showError, options);
  } else {
    result.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function updateShotEndShotPosition(){
  if (navigator.geolocation){
    const options = {enableHighAccuracy: true};
    navigator.geolocation.getCurrentPosition(showEndShotPosition, showError, options);
  } else {
    result.innerHTML = "Geolocation is not supported by this browser.";
  }
}

// ---- Handle geolocation results ----
function showEndPosition(position){
  lat = position.coords.latitude;
  lon = position.coords.longitude;
  document.getElementById("end_latitude").value = lat;
  document.getElementById("end_longitude").value = lon;
  document.getElementById("endHole").submit();
}

function showEndShotPosition(position){
  lat = position.coords.latitude;
  lon = position.coords.longitude;
  document.getElementById("end_shot_latitude").value = lat;
  document.getElementById("end_shot_longitude").value = lon;
  document.getElementById("endShot").submit();
}

function showPosition(position){
  lat = position.coords.latitude;
  lon = position.coords.longitude;
  document.getElementById("id_latitude").value = lat;
  document.getElementById("id_longitude").value = lon;
  document.getElementById("shotForm").submit();
}

function showError(error){
  switch(error.code) {
    case error.PERMISSION_DENIED:
      document.getElementById("result").innerHTML = "Please allow geolocation.";
      break;
    case error.ERR_INTERNET_DISCONNECTED:
      document.getElementById("result").innerHTML = "You have no internet Connection.";
      break;
    case error.TIMEOUT:
      document.getElementById("result").innerHTML = "The request to get user location timed out.";
      break;
  }
}

// ---- Show or hide the map ----
function showMap(){
  document.getElementById("map-container").classList.toggle("hide");
  let btn = document.getElementById("show-map");
  btn.innerHTML = (btn.innerHTML == "Hide Map") ? "Show Map" : "Hide Map";
}

// ---- Colour scorecard cells based on par ----
function colourCells() {
  hole = parseInt(document.getElementById("current-hole").innerText);
  for (let i = 1; i <= hole; i++) {
    let scoreCell = document.getElementById("scor" + i);
    let indicatorCell = document.getElementById("indicator" + i);
    if (parseInt(scoreCell.innerText) > parseInt(document.getElementById("par" + i).innerText)) {
      scoreCell.className = "overpar";
      indicatorCell.className = "overpar1";
    } else if (parseInt(scoreCell.innerText) < parseInt(document.getElementById("par" + i).innerText)) {
      scoreCell.className = "underpar";
      indicatorCell.className = "underpar1";
    } else {
      scoreCell.className = "par";
    }
  }
}

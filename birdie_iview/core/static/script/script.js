addEventListener('DOMContentLoaded', function () {



  let location = document.getElementById("location");
  let map = document.getElementById("show-map");
  let nextHole = document.getElementById("next-hole");
  let currentHole = document.getElementById("current-hole");
  let atMyBall = document.getElementById("at-my-ball");

  // check if the element exists before adding the event listener
  if (location != null){location.addEventListener("click", getLocation);}
  if (map != null){map.addEventListener("click", showMap);}
  if (nextHole != null){nextHole.addEventListener("click", updateShotEndPosition);}
  if (currentHole != null){colourCells();}
  if (atMyBall != null){atMyBall.addEventListener("click", updateShotEndShotPosition);}


  let roundHeadings = document.querySelectorAll('h3.round-heading');

  // Add event listener to each h3 element
  roundHeadings.forEach(heading => {
    heading.addEventListener('click', function () {
      
      // Toggle hide class on the next sibling of the h3 element
      let roundDetails = heading.nextElementSibling;
      roundDetails.classList.toggle('hide');
    });
  });
});
  





// Get the latitude and longitude from browser for shot form
function getLocation()
  {
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showPosition,showError);
    }
  else{result.innerHTML="Geolocation is not supported by this browser.";}
}

function updateShotEndPosition(){
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showEndPosition,showError);
    }
  else{result.innerHTML="Geolocation is not supported by this browser.";}
}

function updateShotEndShotPosition(){
  if (navigator.geolocation)
    {
    navigator.geolocation.getCurrentPosition(showEndShotPosition,showError);
    }
  else{result.innerHTML="Geolocation is not supported by this browser.";}
}


function showEndPosition(position){
  lat=position.coords.latitude;
  lon=position.coords.longitude;
  document.getElementById("end_latitude").value= lat;
  document.getElementById("end_longitude").value= lon;
  document.getElementById("endHole").submit()
}

function showEndShotPosition(position){
  lat=position.coords.latitude;
  lon=position.coords.longitude;
  document.getElementById("end_shot_latitude").value= lat;
  document.getElementById("end_shot_longitude").value= lon;
  document.getElementById("endShot").submit()
}
// add the latitude and longitude to the form and post
function showPosition(position)
  {
  lat=position.coords.latitude;
  lon=position.coords.longitude;
  document.getElementById("id_latitude").value= lat;
  document.getElementById("id_longitude").value= lon;
  document.getElementById("shotForm").submit()
  }

function showError(error)
  {
  switch(error.code)
    {
    case error.PERMISSION_DENIED:
      document.getElementById("result").innerHTML="Please allow geolocation ."
      break;
    case error.ERR_INTERNET_DISCONNECTED:
      document.getElementById("result").innerHTML="You have no internet Connection."
      break;
    case error.TIMEOUT:
      document.getElementById("result").innerHTML="The request to get user location timed out."
      break;
    }
  }

// show or hide the map
function showMap(){
  document.getElementById("map-container").classList.toggle("hide")
  if (document.getElementById("show-map").innerHTML == "Hide Map"){
    document.getElementById("show-map").innerHTML = "Show Map"
  } else {
    document.getElementById("show-map").innerHTML = "Hide Map"
  }

}

function colourCells() {
  hole = parseInt(document.getElementById("current-hole").innerText);
  for (let i = 1; i <= hole; i++) 
  if (parseInt(document.getElementById("scor" + i).innerText) > parseInt(document.getElementById("par" + i).innerText)) {
      document.getElementById("scor" + i).className = "overpar";
  } else if (parseInt(document.getElementById("scor" + i).innerText) < parseInt(document.getElementById("par" + i).innerText)) {
      document.getElementById("scor" + i).className = "underpar";
  } else {
      document.getElementById("scor" + i).className = "par";
  }
}


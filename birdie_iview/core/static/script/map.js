$(document).ready(function () {
    $.ajax({
        url: mapShotsUrl,
        method: 'GET',
        success: function (data) {
            console.log(data);
            getUserLocation(data, roundId);
        }
    });
});

function getUserLocation(data, roundId) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            initMap(data, userLocation, roundId);
        },

            function () {
                handleLocationError(true);
            });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false);
    }
}

function initMap(data, userLocation, roundId) {
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 18,
        mapTypeId: 'satellite',
        center: userLocation // Center of the map
    });

    // Marker for the user's current location
    const userMarker = new google.maps.Marker({
        position: userLocation,
        map: map,
        title: 'You are here'
    });

    // Filter to only include shots from the current round
    if (data) {
        const currentRoundShots = data.filter(function (shot) {
            return shot.round_id === roundId;
        });

        // Separate shot positions by holes
        const holeShots = {};
        currentRoundShots.forEach(shot => {
            if (!holeShots[shot.hole_num]) {
                holeShots[shot.hole_num] = [];
            }
            holeShots[shot.hole_num].push({ lat: parseFloat(shot.latitude), lng: parseFloat(shot.longitude), details: shot });
        });

        // Create polylines for each hole
        for (const holeNum in holeShots) {
            const shotPositions = holeShots[holeNum].map(shot => shot);

            const shotPath = new google.maps.Polyline({
                path: shotPositions,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
            });

            shotPath.setMap(map);

            // Add markers and info windows for each shot
            shotPositions.forEach((shot, index) => {
                const marker = new google.maps.Marker({
                    position: shot,
                    map: map,
                    title: `Shot ${index + 1} - Hole ${holeNum}`,
                });

                const infowindow = new google.maps.InfoWindow({
                    content: `
                        <div>
                            <h3>Hole ${holeNum}</h3>
                            <p><strong>Shot:</strong> ${index + 1}</p>
                            <p><strong>Club:</strong> ${shot.details.club__club_name}</p>
                            <p><strong>Distance:</strong> ${shot.details.shot_distance} Yrds</p>
                        </div>
                    `
                });

                marker.addListener('click', function () {
                    infowindow.open(map, marker);
                });
            });
        }
    }
}




function handleLocationError(browserHasGeolocation) {
    let errorMessage = '';
    if (browserHasGeolocation) {
        errorMessage = 'Error: The Geolocation service failed.';
    } else {
        errorMessage = 'Error: Your browser does not support geolocation.';
    }
    console.error(errorMessage);
}




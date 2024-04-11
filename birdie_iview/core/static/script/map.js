$(document).ready(function () {
    $.ajax({
        url: mapShotsUrl,
        method: 'GET',
        success: function (data) {
            console.log('data', data);
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

async function initMap(data, userLocation, roundId) {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const map = new Map(document.getElementById("map"), {
        zoom: 18,
        mapTypeId: 'satellite',
        center: userLocation, // Center of the map
        mapId: "b2350821306d6b95",
    });

    // Marker for the user's current location
    const userMarker = new AdvancedMarkerElement({
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
            holeShots[shot.hole_num].push({ details: shot });

        });

        console.log('holeshots', holeShots);

        for (const holeNum in holeShots) {
            const shots = holeShots[holeNum];
            shots.forEach(shot => {
                const start = new google.maps.LatLng(parseFloat(shot.details.latitude), parseFloat(shot.details.longitude));
                const end = new google.maps.LatLng(parseFloat(shot.details.end_latitude), parseFloat(shot.details.end_longitude));

                console.log('start', start)
                console.log('end', end)

                const shotPath = new google.maps.Polyline({
                    path: [start, end], // Define the path using start and end points
                    geodesic: true,
                    strokeColor: '#FF0000',
                    strokeOpacity: 1.0,
                    strokeWeight: 3
                });

                shotPath.setMap(map);

            });

            // Add markers and info windows for each shot

            // Define a custom marker icon
            const customMarker = {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: 'blue',
                fillOpacity: 1,
                scale: 6,
                strokeColor: 'white',
                strokeWeight: 2,
            };
            shots.forEach((shot, index) => {
                const marker = new google.maps.Marker({
                    position: new google.maps.LatLng(parseFloat(shot.details.latitude), parseFloat(shot.details.longitude)),
                    map: map,
                    title: `Shot ${index + 1} - Hole ${holeNum}`,
                    icon: customMarker
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




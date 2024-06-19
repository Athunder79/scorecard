$(document).ready(function () {
    $.ajax({
        url: mapShotsUrl,
        method: 'GET',
        success: function (data) {
            console.log('data', data);
            initMap(data, roundId);
        }
    });
});

let map, userMarker;

function initMap(data, roundId) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            loadMap(data, userLocation, roundId);

            // Watch the user's position and update it on the map
            navigator.geolocation.watchPosition(function (position) {
                const newUserLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                updateUserLocation(newUserLocation);
            }, function () {
                handleLocationError(true);
            });

        }, function () {
            handleLocationError(true);
        });
    } else {
        handleLocationError(false);
    }
}

async function loadMap(data, userLocation, roundId) {
    const { Map } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    map = new Map(document.getElementById("map"), {
        zoom: 18,
        mapTypeId: 'satellite',
        center: userLocation, // Center of the map
        mapId: "b2350821306d6b95",
    });

    // Create the flashing blue dot element
    const flashingDot = document.createElement('div');
    flashingDot.className = 'flashing-dot';

    // Custom marker for the user's current location
    userMarker = new AdvancedMarkerElement({
        position: userLocation,
        map: map,
        title: 'You are here',
        content: flashingDot
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
                    strokeColor: 'yellow',
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
                strokeColor: 'blue',
                strokeWeight: 2,
            };

            const endMarker = {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: 'red',
                fillOpacity: 1,
                scale: 3,
                strokeColor: 'red',
                strokeWeight: 2,
            };

            const flagMarker = {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: 'green',
                fillOpacity: 1,
                scale: 3,
                strokeColor: 'green',
                strokeWeight: 2,
            };

            shots.forEach((shot, index) => {
                const isLastShot = index === shots.length - 1;
                const marker = new google.maps.Marker({
                    position: new google.maps.LatLng(parseFloat(shot.details.latitude), parseFloat(shot.details.longitude)),
                    map: map,
                    title: `Shot ${index + 1} - Hole ${holeNum}`,
                    icon: customMarker,
                    label: {
                        text: `${index + 1}`, // Shot number as label text
                        color: 'white', // Label text color
                        fontSize: '12px', // Label font size
                    },

                });

                if (isLastShot && shot.details.end_latitude !== undefined && shot.details.end_longitude !== undefined) {
                    const endMarkerPosition = new google.maps.LatLng(parseFloat(shot.details.end_latitude), parseFloat(shot.details.end_longitude));
                    const endHole = new google.maps.Marker({
                        position: endMarkerPosition,
                        map: map,
                        title: `End of Hole ${holeNum}`,
                        icon: endMarker,
                    });
                }
                console.log('shot', shot.details.shot_num_per_hole)
                console.log('hole number', shot.details.hole_num)

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

function updateUserLocation(newUserLocation) {
    if (userMarker) {
        // Remove the existing marker
        userMarker.setMap(null);
    }

    // Create a new flashing blue dot element
    const flashingDot = document.createElement('div');
    flashingDot.className = 'flashing-dot';

    // Create a new marker at the new location
    userMarker = new google.maps.marker.AdvancedMarkerElement({
        position: newUserLocation,
        map: map,
        title: 'You are here',
        content: flashingDot
    });

    // Center the map on the new user location
    map.setCenter(newUserLocation);
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

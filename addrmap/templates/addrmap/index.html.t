{% comment %}
This is the template file for the single-page app.  No data is originally 
needed, so there is not much templating used.  This file acts as the central
point for the front end, containing the HTML and Javascript for the page. 
{% endcomment %}

<!DOCTYPE html>
{% load staticfiles %}
<html lang="en">
<head>
  <link rel="stylesheet" type="text/css" href="{% static 'addrmap/smt.css' %}" />
  <title>Address Lister -- Messick</title>
  <link rel="icon" type="image/gif" href="{% static 'addrmap/icon.gif' %}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="content-type" content="text/html;charset=utf-8" />
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>    
  <script src="https://maps.googleapis.com/maps/api/js?key={{ apikey }}"></script>  
  <script src="{% static 'addrmap/smt.js' %}"></script>
<script>
var markers = [];
function refreshList(addrList){
    // refresh onscreen list based on inpassed address list.
    
    // would be more efficient to only add each address when clicked,
    // but that would fail if multiple users are updating the list.
    $('#addresstable tr.addrdata').remove();
    for (addr of addrList) {
      $('#addresstable tr:last-child').after('<tr class="addrdata"><td>'
                                    +Number((addr.lng).toFixed(2))+'</td><td>'
                                    +Number((addr.lat).toFixed(2))+'</td><td>'
                                    +addr.desc+'</td></tr>');
    }                                  

    // refresh markers from fusion table.
    // google api supposedly has smooth integration here, using fusion 
    // table layers, but it all was awkward and slow, so handling it directly:
    $.ajax({
        url : "https://www.googleapis.com/fusiontables/v2/query?sql=SELECT%20*%20FROM%20{{tablekey}}&key={{apikey}}", 
        method : "GET", 
        cache: false,
        success : function(json) {
            for (var i = 0; i < markers.length; i++) {
              markers[i].setMap(null);
            }
            markers=[]
            if (json.rows != null) {
              for (row of json.rows) {
                // lat and lng are in fusion table col 1 and 2
                latLng = new google.maps.LatLng(row[1], row[2]); 
                var marker = new google.maps.Marker({
                  position: latLng,
                  map: map
                });
                markers.push(marker)
              }
            }
        },
        error : function(xhr,errmsg,err) {
            window.alert(xhr.statusText);
            console.log(xhr); 
        }
    });

}

function submitAddress(newaddr) {
    // post new address to server
    
    /* because of the google fusion access, things are slow.  
       let the user know with a wait cursor. if multiple clicks
       are being processed at once, the first to finish will clear
       the wait cursor; if this were a problem, we could add a counting 
       semaphore.  */
    $("html").addClass("wait");
    $.ajax({
        url : "{% url 'addrmap:address_add' %}", 
        method : "POST", 
        data : newaddr, 
        success : function(jsondata) {
            refreshList(jsondata);
            $("html").removeClass("wait");
        },
        error : function(xhr,errmsg,err) {
            $("html").removeClass("wait");
            window.alert(xhr.statusText);
            console.log(xhr); 
        }
    });
};

function clearAddresses() {
    $("html").addClass("wait"); // show wait cursor
    
    $.ajax({
        url : "{% url 'addrmap:address_trunc' %}",
        method : "POST",
        success : function(jsondata) {
            refreshList(jsondata);
            $("html").removeClass("wait");
        },
        error : function(xhr,errmsg,err) {
            $("html").removeClass("wait");
            window.alert(xhr.statusText);
            console.log(xhr); 
        }});
};

var map;
var geocoder;
function initialize() {
  // initialize map
  var mapProp = {
    // arbitrarily start map on BsAs, Argentina
    center:new google.maps.LatLng(-34.6, -58.4), 
    appxrad_m: 20000, // appx radius of map
    scaleControl: true,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var circ = new google.maps.Circle();
  circ.setRadius(mapProp.appxrad_m);
  circ.setCenter(mapProp.center);   
  map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
  geocoder = new google.maps.Geocoder; 
  map.setCenter(mapProp.center);
  map.fitBounds(circ.getBounds());

  // add click behavior: reverse geolocate and if valid, submit new address
  google.maps.event.addListener(map, 'click', function(event) {
    geocoder.geocode({'location': event.latLng}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK 
                && results[0] 
                && results[0].types.includes('street_address')) {
            // we have results; tell back end to add to our list.
            submitAddress({'lat': event.latLng.lat(),
                           'lng': event.latLng.lng(),
                           'desc': results[0]['formatted_address']})
        } else {
            window.alert('No address found for this location.');
        }
      });
  });

  // get initial state of the address list
  $.ajax({
        url : "{% url 'addrmap:address_get' %}",
        method : "GET",

        // handle a successful response
        success : function(jsondata) {
            refreshList(jsondata);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            window.alert(xhr.statusText);
            console.log(xhr); 
        }});

}
google.maps.event.addDomListener(window, 'load', initialize);
</script>

</head>

<body>
<div id="mapholder">
  <div id="googleMap"></div>
</div>

<div class="row">
<div id="listtitle">Selected Addresses:</div>
<div id="actionbuttonholder">
<button class="actionbutton" onClick="clearAddresses()">Clear Addresses</button>
</div>
</div>

<div id="addresslistholder">
<table id="addresstable">
<tr><th>Longitude</th><th>Latitude</th><th class="addressdesc">Address</th></tr>
</table>

</div>
</body>
</html>

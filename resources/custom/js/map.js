// HEREMap implementation
{
    // marker colors
    INACTIVE_COLOR = '#1D71CC';
    ACTIVE_COLOR = '#000000';

    // constructor
    // default_layers is the data which is needed from the platform that is instantiated outside of this class
    // entity_id is the ID of the HTML element that works as the map container
    function HEREMap(default_layers, entity_id) {
        this.default_layers = default_layers;
        this.map = new H.Map(document.getElementById(entity_id), default_layers.normal.map);
        this.behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(this.map));
        // UI elements like zoom-in/zoom-out buttons
        this.ui = H.ui.UI.createDefault(this.map, this.default_layers);

        // list of all added markers
        this.markers = [];
        // markers that shall form the viewport
        this.viewport_marker_group = new H.map.Group();
        this.map.addObject(this.viewport_marker_group);
    }

    // method for generating the marker icon with the given color
    HEREMap.prototype.createSVGMarkup = function(color) {
        // https://developer.mozilla.org/en-US/docs/Web/SVG/Element/path
        var svgMarkup =
                '<svg width="28" height="35" xmlns="http://www.w3.org/2000/svg">' +
                    '<g>' +
                        '<ellipse cx="15" cy="32" rx="6.5" ry="3" fill="#BBBBBB" style="fill-opacity:0.7"/>' +
                        '<path d="M 15 30 l -8 -8 a 12 12 0 1 1 16 0 z" stroke="white" stroke-width="2" fill="' + color + '" />' +
                    '</g>' +
                '</svg>';

        return new H.map.Icon(svgMarkup);
    };

    // creates the actual marker instance at the given location with the given color
    HEREMap.prototype.createMarker = function(lat, lon, color) {
        return new H.map.Marker({lat: lat, lng: lon}, {icon: this.createSVGMarkup(color)});
    };

    // adds an inactive marker to the map with the given data
    // this marker will contribute to the initial viewport of the map when calling setViewport() if is_viewport_marker is defined and true
    HEREMap.prototype.addMarker = function(lat, lon, id, data, is_viewport_marker) {
        // create marker and set data
        var marker = this.createMarker(lat, lon, INACTIVE_COLOR);
        marker.setData({
            id: id,
            data: data
        });

        // add marker to the list of markers
        this.markers.push(marker);
        // and to the map
        this.map.addObject(marker);

        if (is_viewport_marker) {
            // add the marker to the viewport_marker_group as well
            this.viewport_marker_group.addObject(marker);
        }
    };

    // convenient method for adding a viewport marker
    HEREMap.prototype.addViewportMarker = function(lat, lon, marker_id, marker_data) {
        this.addMarker(lat, lon, marker_id, marker_data, true);
    };

    // sets the viewport of the map based on the viewport markers or the given default coordinates
    HEREMap.prototype.setViewport = function(default_lat, default_lon, default_zoom) {
        if (this.viewport_marker_group.getObjects().length == 0) {
            // use the default settings if no viewport marker is set
            this.map.setCenter({lat: default_lat, lng: default_lon});
            this.map.setZoom(default_zoom);
        } else {
            this.map.setViewBounds(this.viewport_marker_group.getBounds());
            // zoom to the default level, if only one viewport marker is set
            if (this.viewport_marker_group.getObjects().length == 1) {
                this.map.setZoom(default_zoom);
            }
        }
    }

    // you can register special events for additional functionality
    HEREMap.prototype.registerEventListener = function(callback) {
        var active_marker_icon = this.createSVGMarkup(ACTIVE_COLOR);
        var inactive_marker_icon = this.createSVGMarkup(INACTIVE_COLOR);
        // save markers in a locale variable in order to make the list visible to the inner function
        var markers = this.markers;
        this.map.addEventListener('tap', function(evt) {
            var target = evt.target;
            if (target instanceof H.map.Marker) {
                // iterate over all markers to make them inactive
                for (var i = 0; i < markers.length; i++) {
                    markers[i].setIcon(inactive_marker_icon);
                }

                // activate the target marker
                target.setIcon(active_marker_icon);

                // run the callback method
                callback(target.getData().id, target.getData().data);
            }

        });
    };

    HEREMap.prototype.showOnly = function(marker_ids) {
        for (var i = 0; i < this.markers.length; i++) {
            var marker = this.markers[i];

            if ($.inArray(marker.getData().id, marker_ids) > -1) {
                marker.setVisibility(true);
            } else {
                marker.setVisibility(false);
            }
        }
    };
}

/*
 * Required scripts:
 *   <link rel="stylesheet" type="text/css" href="https://js.api.here.com/v3/3.0/mapsjs-ui.css" />
 *   <script type="text/javascript" charset="UTF-8" src="https://js.api.here.com/v3/3.0/mapsjs-core.js"></script>
 *   <script type="text/javascript" charset="UTF-8" src="https://js.api.here.com/v3/3.0/mapsjs-service.js"></script>
 *   <script type="text/javascript" charset="UTF-8" src="https://js.api.here.com/v3/3.0/mapsjs-ui.js"></script>
 *   <script type="text/javascript" charset="UTF-8" src="https://js.api.here.com/v3/3.0/mapsjs-mapevents.js"></script>
 *   <script type="text/javascript" charset="UTF-8" src="https://code.jquery.com/jquery-1.11.3.min.js"></script>
 *
 * Sample code for instantiating the platform and instantiating the map, adding some data
 * var platform = new H.service.Platform({
 *   app_id: 'mZIEtVjJGeugdntBBM7B',
 *   app_code: 'QyYAEUpGd0Nt0DDfh94YAA',
 *   useCIT: true,
 *   useHTTPS: true
 * });
 *
 * // instantiates the map and draws it into a div with the ID 'map'
 * var map_instance = new HEREMap(platform.createDefaultLayers(), 'map');
 *
 * // sets a viewport marker that is used for setting the initial viewport of the map
 * map_instance.addViewportMarker(52.5159, 13.3777, "marker_0", "Marker Data 0");
 * // sets a marker that is not used for the initial viewport
 * map_instance.addMarker(52.5159, 13.3877, "marker_1", "Marker Data 1");
 *
 * // this adds an event listener that will be called if a marker was activated
 * map_instance.registerEventListener(function(id, data) {
 *  // just looks for an element with the ID content and sets its content to the marker data
 * 	$('#content').text(data);
 * });
 *
 * // sets the initial viewport
 * map_instance.setViewport(51.5159, 13.3777, 14);
 */
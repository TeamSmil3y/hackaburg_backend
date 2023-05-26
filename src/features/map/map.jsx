import { useState, useEffect } from "react";
import AppendHead from 'react-append-head';
import mapboxgl, {LngLat, LngLatLike} from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { QueryClient, QueryClientProvider, useQuery } from 'react-query'
const queryClient = new QueryClient()


const fetch_hubs = () => {
    return []
}

const get_location = () => {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const loc = [position.coords.longitude, position.coords.latitude];
                resolve(loc);
                },
            (error) => {
                reject(error);
            }
        );
    });
};

export const Map = () => {

    useEffect(() => {
    const func = async () => {
    var map = null
    try {
      var loc = await get_location();

      // Render map
      map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: loc,
        zoom: 11
      });

      // Rest of your map-related code...
    } catch (error) {
            console.error('Error retrieving location:', error);
    }

        map.on("load", () => {
            map.loadImage(
                "https://docs.mapbox.com/mapbox-gl-js/assets/cat.png",
                (error, image)  => {
                    if (error) throw error;
                    map.addImage('cat', image);
                }
            )

            fetch("http://localhost:80/get_hubs/").then((r)=>{r.json().then((j)=>{
                j = JSON.parse(j)
                for (var i = 0; i < j.length; i++) {
                    var element = j[i]
                    console.warn(element)
                    map.addSource(element["pk"], {
                        'type': 'geojson',
                        'data': {
                            'type': 'FeatureCollection',
                            'features': [
                                {
                                    'type': 'Feature',
                                    'geometry': {
                                        'type': 'Point',
                                        'coordinates': [element["fields"]["longitude"], element["fields"]["latitude"]],
                                    }
                                }
                            ]
                        }
                    });

                    // Add a layer to use the image to represent the data.
                    map.addLayer({
                        'id': element["pk"],
                        'type': 'symbol',
                        'source': element["pk"], // reference the data source
                        'layout': {
                            'icon-image': 'circle', // reference the image
                            'icon-size': 0.2
                        }
                    });
                };
            })})
    })
  };

  func();
  }, []);
    mapboxgl.accessToken = 'pk.eyJ1IjoibHN0dW1hIiwiYSI6ImNsaTN0dnc3ZDBpMTkzZW1seml3NTZobDUifQ._Fo8j6VzHhLj-BDC5EW_xg';

    return (
        <div style={{display: "grid"}}>
            <div id="map"></div>
            <AppendHead>
                <link href='https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css' rel='stylesheet' />
                <script src="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js" defer></script>
            </AppendHead>
        </div>
    )
}

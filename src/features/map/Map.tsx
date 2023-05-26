import { useState, useEffect, useRef } from "react";
import { v4 as uuid } from 'uuid'
import AppendHead from 'react-append-head';
import { LngLat, LngLatLike, Map as MapBox, AnyLayer } from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';


const getLocation = (): Promise<Loc> => {
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

type Loc = [number, number]
type Hub = {
  loc: Loc,
  // type: 'official' | 'community'
}

type Props = {
  hubs?: Hub[],
  cars?: null[]
}

const getHubConfig = ({ loc }: Hub) => ({
  id: uuid(),
  type: 'circle',
  source: {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [loc[0], loc[1]]
          }
        }
      ]
    }
  },
  paint: {
    'circle-radius': 6, // Adjust the radius of the circle
    'circle-color': '#FF0000' // Specify the color of the circle
  }
} as AnyLayer)

export const Map = ({ hubs, cars }: Props) => {
  const map = useRef<MapBox | null>(null);

  useEffect(() => {
    const asyncWrapper = async () => {
      map.current = new MapBox({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: await getLocation(),
        zoom: 11,
        accessToken: 'pk.eyJ1IjoibHN0dW1hIiwiYSI6ImNsaTN0dnc3ZDBpMTkzZW1seml3NTZobDUifQ._Fo8j6VzHhLj-BDC5EW_xg'
      })
      console.log(map.current)
    }
    asyncWrapper()
  }, [])

  useEffect(() => {
    if (!map.current) return;

    // TODO: clear map

    if (hubs) {
      hubs.forEach((hub) => {
        const config = getHubConfig(hub);
        // TODO: save ID
        map.current?.addLayer(config)
      })
    }

  }, [hubs, cars])

  // if (m)


//   useEffect(() => {
//     const func = async () => {
{/*    const loc = await get_location();*/}

{/*    // Render map*/}

{/*    map.on("load", () => {*/}
{/*      map.addLayer({*/}
{/*        id: 'a',*/}
{/*        type: ''*/}
//       })
//       map.loadImage(
{/*          "https://docs.mapbox.com/mapbox-gl-js/assets/cat.png",*/}
{/*          (error, image)  => {*/}
{/*              if (error) throw error;*/}
{/*              map.addImage('circle', image);*/}
{/*          }*/}
{/*      )*/}

{/*        fetch("http://localhost:80/get_hubs/").then((r)=>{r.json().then((j)=>{*/}
{/*            j = JSON.parse(j)*/}
{/*            for (let i = 0; i < j.length; i++) {*/}
{/*                const element = j[i]*/}
//                 console.warn(element)
//                 map.addSource(element["pk"], {
{/*                    'type': 'geojson',*/}
{/*                    'data': {*/}
{/*                        'type': 'FeatureCollection',*/}
{/*                        'features': [*/}
{/*                            {*/}
{/*                                'type': 'Feature',*/}
{/*                                'geometry': {*/}
{/*                                    'type': 'Point',*/}
{/*                                    'coordinates': [element["fields"]["longitude"], element["fields"]["latitude"]],*/}
//                                 }
{/*                            }*/}
{/*                        ]*/}
{/*                    }*/}
//                 });
//
//                 // Add a layer to use the image to represent the data.
//                 map.addLayer({
//                     'id': element["pk"],
//                     'type': 'symbol',
//                     'source': element["pk"], // reference the data source
//                     'layout': {
{/*                        'icon-image': 'circle', // reference the image*/}
//                         'icon-size': 0.2
//                     }
//                 });
//             }
//         })})
// })
// };
//
// func();
// }, []);
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

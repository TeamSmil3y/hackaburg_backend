import { useState, useEffect } from "react";
import AppendHead from 'react-append-head';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { QueryClient, QueryClientProvider, useQuery } from 'react-query'
const queryClient = new QueryClient()


const fetch_hubs = () => {
    return []
}
fetch_hubs()

const get_location: float[] = async () => {
    let loc = [0, 0]
    await navigator.geolocation.getCurrentPosition((position) => {
        loc = [position.coords.latitude, position.coords.longitude]
        console.log("ll" + loc)
    })
    return loc
}

export const Map = () => {
    const [location, setLocation] = useState([0, 0])
    useEffect(() => {
        const func = async () => { console.log("gl " + await get_location()) }
        func()
    }, [])
    console.log(location)
    mapboxgl.accessToken = 'pk.eyJ1IjoibHN0dW1hIiwiYSI6ImNsaTN0dnc3ZDBpMTkzZW1seml3NTZobDUifQ._Fo8j6VzHhLj-BDC5EW_xg';
    setTimeout(() => {const map: mapboxgl.Map = new mapboxgl.Map({
        container: 'map', // container ID
        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
        style: 'mapbox://styles/mapbox/streets-v12', // style URL
        center: location, // starting position [lng, lat]
        zoom: 9 
    })}, 50);
    
    
    
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

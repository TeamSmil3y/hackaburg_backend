var email;
var password;

function authorize(email, password)
{
    // base64 encoded basic auth username:password@web.site
    var creds = btoa(email + ":" + password)
    return "Basic " + creds
}

export async function post(path, body) {
    let request = await fetch("https://api.hubhopper.app"+path, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "Authorization": authorize(email, password)
        }
    });
    return await request.json()
}

export async function find_rides(destination_hub_id, source_hub_id) {
    return await post('/find-rides/', {'destination_hub_id':destination_hub_id, 'source_hub_id':source_hub_id})
}
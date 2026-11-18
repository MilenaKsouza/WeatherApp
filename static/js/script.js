const searchButton = document.getElementById("searchButton");
const cityInput = document.getElementById("cityInput");

async function searchWeather() {
    const city = cityInput.value.trim();

    if (!city) {
        document.getElementById("errorMessage").textContent =
            "Digite o nome de uma cidade.";
        return;
    }

    const errorMessage = document.getElementById("errorMessage");
    errorMessage.textContent = "Buscando informações...";

    try {
        const response = await fetch(
            `/weather?city=${encodeURIComponent(city)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erro ao consultar o clima.");
        }

        document.getElementById("cityName").textContent = data.city;
        document.getElementById("temperature").textContent =
            `${data.temperature}°C`;
        document.getElementById("description").textContent = data.description;
        document.getElementById("humidity").textContent = `${data.humidity}%`;
        document.getElementById("wind").textContent = `${data.wind} km/h`;
        document.getElementById("feelsLike").textContent =
            `${data.feels_like}°C`;

        errorMessage.textContent = "";

    } catch (error) {
        errorMessage.textContent = error.message;
    }
}

searchButton.addEventListener("click", searchWeather);

cityInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        searchWeather();
    }
});

function parseDate(date) {
    let year = date.getFullYear()
    let month = date.getMonth()
    let day = date.getDate()
    if (month >= 0 && month < 10) {
        month = '0' + (month + 1)
    }
    if (day >= 1 && day < 10) {
        day = '0' + day
    }
    return year + '-' + month + '-' + day
}

function weekDayName(day) {
    if (day == 0) {
        return "Sun"
    }
    if (day == 1) {
        return "Mon"
    }
    if (day == 2) {
        return "Tue"
    }
    if (day == 3) {
        return "Wed"
    }
    if (day == 4) {
        return "Thu"
    }
    if (day == 5) {
        return "Fri"
    }
    if (day == 6) {
        return "Sat"
    }
    return ""

}

function getDaysOfThisWeek() {
    const today = new Date()
    let date = today.getDate()
    let weekDay = today.getDay()
    if (weekDay == 0) {
        weekDay = 7
    }
    let result = []
    for (let i = weekDay; i >= 1; --i) {
        today.setDate(date - i)
        result.push(parseDate(today))
    }
    return result
}

const { createApp } = Vue;

const metabolismApp = Vue.createApp({
    data() {
        return {
            metabolismData: {
                exercise_metabolism: 0,
                bmr: 0,
                intake: 0,
                total: 0
            }
        };
    },
    mounted() {
        fetch('/nutrition/metabolism/')
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    const latestData = data[0];
                    this.metabolismData = latestData;
                }
                console.log('Today metabolism:', data);
            })
            .catch(error => console.error('Error:', error));
    },
    compilerOptions: {
        delimiters: ["[[", "]]"]
    }
}).mount('#metabolism-app');


const barApp = createApp({
    mounted() {
        this.loadMetabolismDataThisWeek();
    },
    data() {
        return {
            weeklyMetabolismData: [],
            maxBarHeight: 300,  // maximum bar height in px
            scale: 1
        };
    },
    methods: {
        calculateScale() {
            const maxValue = Math.max(...this.weeklyMetabolismData.map(item => Math.abs(item.total)));
            if (maxValue > this.maxBarHeight) {
                this.scale = this.maxBarHeight / maxValue;
            } else {
                this.scale = 1;
            }
        },
        barStyle(n) {
            const height = Math.abs(n) * this.scale;
            const isPositive = n >= 0;
            return {
                height: `${height}px`,
                backgroundColor: isPositive ? '#FF5722': '#4CAF50',
                boxShadow: '2px 2px 8px rgba(0, 0, 0, 0.2)',
                borderRadius: '5px'
            };
        },
        loadMetabolismDataThisWeek() {
            fetch('/nutrition/metabolism_7days/')
                .then(response => response.json())
                .then(data => {
                    this.weeklyMetabolismData = data.map((item) => {
                        const dayName = weekDayName(new Date(item.date).getDay());
                        const total = item.total;
                        return { day: dayName, total: total };
                    });
                    this.calculateScale();
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
    },
    compilerOptions: {
        delimiters: ["[[", "]]"]
    }
}).mount('#calorie-bar-app');

const pieApp = createApp({
    mounted() {
        this.loadTodayIntake()
    },
    data() {
        return {
            today: new Date().toDateString(),
            intake: {
                fat: 0, carbohydrate: 0, protein: 0, other: 0
            }
        }
    },
    methods: {
        loadTodayIntake() {
            fetch('/nutrition/food_daily/')
                .then(response => response.json())
                .then(data => {
                    this.intake = data;
                });
        },
        pieStyle() {
			if (this.intake.fat == 0 && this.intake.carbohydrate == 0 && this.intake.protein == 0) {
				return `background:
				conic-gradient(from 0deg,
						#f0f0f0 0,
						#f0f0f0 calc(100%)
				)`
			} else {
				return `background:
				conic-gradient(from 0deg,
						#037ffc 0,
						#037ffc calc(${this.intake.fat}%),
						#21cc99 calc(${this.intake.fat}%),
						#21cc99 calc(${this.intake.fat + this.intake.carbohydrate}%),
						#db5625 calc(${this.intake.fat + this.intake.carbohydrate}%),
						#db5625 calc(${this.intake.fat + this.intake.carbohydrate + this.intake.protein}%),
						#fce158 calc(${this.intake.fat + this.intake.carbohydrate + this.intake.protein}%),
						#fce158 calc(100%)
				)`
			}
        }
    },
    compilerOptions: {
        delimiters: ["[[", "]]"]
    }
}).mount('#calorie-pie-app')

var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()  // 使用OpenStreetMap瓦片
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([0, 0]),  // 默认中心点
        zoom: 2  // 默认缩放级别
    })
});
var userLocationCoords;
function addLocationMarker(position) {
    userLocationCoords = ol.proj.fromLonLat([position.coords.longitude, position.coords.latitude]);
    var markerStyle = new ol.style.Style({
        image: new ol.style.Icon({
            src: 'https://maps.google.com/mapfiles/ms/icons/green-dot.png', // 绿色图标的 URL
            scale: 0.8 // 调整图标大小
        })
    });
    var marker = new ol.Feature({
        geometry: new ol.geom.Point(userLocationCoords),
    });

    marker.setStyle(markerStyle);

    var vectorSource = new ol.source.Vector({
        features: [marker],
    });

    var markerVectorLayer = new ol.layer.Vector({
        source: vectorSource,
    });

    map.addLayer(markerVectorLayer);
    map.getView().setCenter(userLocationCoords);
    map.getView().setZoom(15);

    // 获取附近健身房
    fetchNearbyGyms(position.coords.latitude, position.coords.longitude);
}
function fetchNearbyGyms(latitude, longitude) {
    var radius = 5000; // 搜索半径，单位是米
    var query = `
    [out:json];
    (
      node["leisure"="fitness_centre"](around:${radius},${latitude},${longitude});
      node["amenity"="gym"](around:${radius},${latitude},${longitude});
      node["sport"="fitness"](around:${radius},${latitude},${longitude});
    );
    out center;
    out tags;
    `;

    fetch('https://overpass-api.de/api/interpreter?data=' + encodeURIComponent(query))
        .then(response => response.json())
        .then(data => {
            var gymListElement = document.getElementById('gym-list');
            gymListElement.innerHTML = '';

            data.elements.forEach(element => {
                if (!element.tags.name || !element.tags['addr:street'] || typeof element.lat === 'undefined' || typeof element.lon === 'undefined') {
                    return;  // If there is no name, street information, or valid coordinates, skip this element
                }
                var coords = ol.proj.fromLonLat([element.lon, element.lat]);
                var feature = new ol.Feature({
                    geometry: new ol.geom.Point(coords),
                });

                var style = new ol.style.Style({
                    image: new ol.style.Icon({
                        color: 'red',
                        crossOrigin: 'anonymous',
                        src: 'data:image/svg+xml;utf8,<svg fill="%23ff0000" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30" width="40px" height="40px"><circle cx="15" cy="15" r="15"/></svg>',
                        scale: 0.5,
                    }),
                });

                feature.setStyle(style);

                var vectorSource = new ol.source.Vector({
                    features: [feature],
                });

                var markerVectorLayer = new ol.layer.Vector({
                    source: vectorSource,
                });

                map.addLayer(markerVectorLayer);

                // 添加详细信息到列表
                var listItem = document.createElement('li');
                listItem.textContent = `${element.tags.name}, ${element.tags['addr:street']}, ${element.tags['addr:postcode'] ? element.tags['addr:postcode'] : 'No postcode info'}`;
                listItem.classList.add('clickable-list-item');
                listItem.onclick = function () {
                    map.getView().setCenter(coords);
                    map.getView().setZoom(18);
                };
                gymListElement.appendChild(listItem);
            });

            document.getElementById('back-to-user-location').onclick = function () {
                if (userLocationCoords) {
                    map.getView().setCenter(userLocationCoords);
                    map.getView().setZoom(15);
                }
            };

        });
}


if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (position) {
        addLocationMarker(position);
    }, function (error) {
        console.log("Error occurred. Error code: " + error.code);
    });
} else {
    console.log("Geolocation is not supported by this browser.");
}

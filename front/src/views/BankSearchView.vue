<template>
  <div class="container">
    <div class="sidebar">
      <label>광역시 / 도</label>
      <select v-model="sido" @change="updateSigungu">
        <option value="">광역시 / 도 선택</option>
        <option v-for="region in mapData.mapInfo" :key="region.name" :value="region.name">{{ region.name }}</option>
      </select>

      <label>시 / 군 / 구</label>
      <select v-model="sigungu">
        <option value="">시 / 군 / 구 선택</option>
        <option v-for="name in sigunguList" :key="name" :value="name">{{ name }}</option>
      </select>

      <label>은행</label>
      <select v-model="bank">
        <option value="">은행 선택</option>
        <option v-for="bank in mapData.bankInfo" :key="bank" :value="bank">{{ bank }}</option>
      </select>

      <button @click="searchBank">찾기</button>
    </div>
    <div id="map" style="flex-grow: 1; height: 100vh;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const map = ref(null)
const markers = ref([])
const polyline = ref(null)
const sido = ref('')
const sigungu = ref('')
const bank = ref('')
const sigunguList = ref([])
const mapData = ref({ mapInfo: [], bankInfo: [] })
const infowindow = ref(null)
const kakaoReady = ref(false) // ✅ 지도 로드 상태 추적

function updateSigungu() {
  const region = mapData.value.mapInfo.find(r => r.name === sido.value)
  sigunguList.value = region ? region.countries : []
}

function initMap() {
  console.log('✅ 지도 초기화 중')
  const mapContainer = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(37.49818, 127.027386),
    level: 3
  }
  map.value = new kakao.maps.Map(mapContainer, options)
  infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 })
  kakaoReady.value = true
  console.log('✅ kakaoReady = true 설정됨')
}


function searchBank() {
  if (!kakaoReady.value) {
    alert('지도가 아직 로드되지 않았습니다. 잠시 후 다시 시도해주세요.')
    return
  }

  if (!sido.value || !sigungu.value || !bank.value) {
    alert('모든 항목을 선택해주세요.')
    return
  }

  const keyword = `${sido.value} ${sigungu.value} ${bank.value}`
  const ps = new kakao.maps.services.Places()

  markers.value.forEach(m => m.setMap(null))
  markers.value = []
  if (infowindow.value) infowindow.value.close()
  if (polyline.value) polyline.value.setMap(null)

  ps.keywordSearch(keyword, function (data, status) {
    if (status === kakao.maps.services.Status.OK) {
      const bounds = new kakao.maps.LatLngBounds()

      data.forEach(place => {
        const position = new kakao.maps.LatLng(place.y, place.x)
        const marker = new kakao.maps.Marker({ position, map: map.value })
        markers.value.push(marker)
        bounds.extend(position)

        kakao.maps.event.addListener(marker, 'click', function () {
          const content = `<div style="padding:5px;font-size:13px;">${place.place_name}</div>`
          infowindow.value.setContent(content)
          infowindow.value.setPosition(position)
          infowindow.value.setMap(map.value)

          const origin = '127.039585,37.501274'
          const destination = `${place.x},${place.y}`

          fetch(`https://apis-navi.kakaomobility.com/v1/directions?origin=${origin}&destination=${destination}&priority=RECOMMEND`, {
            headers: { Authorization: `KakaoAK ${window.config.restApiKey}` }
          })
            .then(res => res.json())
            .then(result => {
              const coords = result.routes[0].sections[0].roads.flatMap(r => r.vertexes)
              const path = []
              for (let i = 0; i < coords.length; i += 2) {
                path.push(new kakao.maps.LatLng(coords[i + 1], coords[i]))
              }

              if (polyline.value) polyline.value.setMap(null)
              polyline.value = new kakao.maps.Polyline({
                path: path,
                strokeWeight: 5,
                strokeColor: '#007bff',
                strokeOpacity: 0.8,
                strokeStyle: 'solid'
              })
              polyline.value.setMap(map.value)
            })
        })
      })

      if (map.value) map.value.setBounds(bounds)
    } else {
      alert('검색 결과가 없습니다.')
    }
  })
}

onMounted(async () => {
  try {
    const res = await fetch('/data.json');
    if (!res.ok) throw new Error('Failed to fetch data.json');
    mapData.value = await res.json();
  } catch (e) {
    console.error(e);
    mapData.value = { mapInfo: [], bankInfo: [] };
  }

  const ensureKakaoMap = () => {
    if (window.kakao && window.kakao.maps && kakao.maps.load) {
      console.log("✅ Kakao Maps SDK 로드 성공, initMap 실행");
      kakao.maps.load(initMap);
    } else {
      console.log("📌 Kakao SDK가 아직 없으므로 script 동적 추가");
      const script = document.createElement('script');
      script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=0af238b62ebee50a156ca780853b0f6b&libraries=services';
      script.onload = () => {
        console.log("✅ Kakao Maps SDK script.onload 실행");
        kakao.maps.load(initMap);
      };
      document.head.appendChild(script);
    }
  };

  ensureKakaoMap();
});



</script>

<style scoped>
.container {
  display: flex;
}
.sidebar {
  width: 300px;
  padding: 1rem;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>

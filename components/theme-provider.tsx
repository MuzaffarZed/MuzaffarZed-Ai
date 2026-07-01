"use client"

import { createContext, useContext, useEffect, useState, ReactNode } from "react"

type Theme = "light" | "dark"
type BackgroundTheme = {
  id: string
  name: string
  type: "solid" | "image"
  value: string
  category: string
}

interface ThemeContextType {
  theme: Theme
  setTheme: (theme: Theme) => void
  backgroundTheme: BackgroundTheme
  setBackgroundTheme: (bg: BackgroundTheme) => void
  backgrounds: BackgroundTheme[]
}

const defaultBackground: BackgroundTheme = {
  id: "default",
  name: "Standart",
  type: "solid",
  value: "bg-background",
  category: "solid"
}

// 100+ background themes
const backgrounds: BackgroundTheme[] = [
  // Solid colors
  { id: "default", name: "Standart", type: "solid", value: "bg-background", category: "solid" },
  { id: "ocean", name: "Okean", type: "solid", value: "bg-gradient-to-br from-blue-900 via-blue-800 to-cyan-900", category: "solid" },
  { id: "sunset", name: "Quyosh botishi", type: "solid", value: "bg-gradient-to-br from-orange-500 via-pink-500 to-purple-600", category: "solid" },
  { id: "forest", name: "O'rmon", type: "solid", value: "bg-gradient-to-br from-green-900 via-emerald-800 to-teal-900", category: "solid" },
  { id: "midnight", name: "Yarim tun", type: "solid", value: "bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900", category: "solid" },
  
  // Nature images
  { id: "nature1", name: "Tog'lar", type: "image", value: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80", category: "tabiyat" },
  { id: "nature2", name: "O'rmon", type: "image", value: "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1920&q=80", category: "tabiyat" },
  { id: "nature3", name: "Dengiz", type: "image", value: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80", category: "tabiyat" },
  { id: "nature4", name: "Sharshara", type: "image", value: "https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=1920&q=80", category: "tabiyat" },
  { id: "nature5", name: "Gul", type: "image", value: "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1920&q=80", category: "tabiyat" },
  { id: "nature6", name: "Yashil dala", type: "image", value: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80", category: "tabiyat" },
  { id: "nature7", name: "Ko'l", type: "image", value: "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=1920&q=80", category: "tabiyat" },
  { id: "nature8", name: "Qor", type: "image", value: "https://images.unsplash.com/photo-1517299321609-52687d1bc55a?w=1920&q=80", category: "tabiyat" },
  { id: "nature9", name: "Sahro", type: "image", value: "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=1920&q=80", category: "tabiyat" },
  { id: "nature10", name: "Kamalak", type: "image", value: "https://images.unsplash.com/photo-1507400492013-162706c8c05e?w=1920&q=80", category: "tabiyat" },
  { id: "nature11", name: "Bahor", type: "image", value: "https://images.unsplash.com/photo-1462275646964-a0e3571f4f7c?w=1920&q=80", category: "tabiyat" },
  { id: "nature12", name: "Kuz", type: "image", value: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1920&q=80", category: "tabiyat" },
  
  // Space/Cosmos
  { id: "space1", name: "Galaktika", type: "image", value: "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=80", category: "kosmos" },
  { id: "space2", name: "Yulduzlar", type: "image", value: "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920&q=80", category: "kosmos" },
  { id: "space3", name: "Oy", type: "image", value: "https://images.unsplash.com/photo-1446941611757-91d2c3bd3d45?w=1920&q=80", category: "kosmos" },
  { id: "space4", name: "Nebula", type: "image", value: "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=1920&q=80", category: "kosmos" },
  { id: "space5", name: "Saturn", type: "image", value: "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=1920&q=80", category: "kosmos" },
  { id: "space6", name: "Quyosh", type: "image", value: "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=1920&q=80", category: "kosmos" },
  { id: "space7", name: "Yer", type: "image", value: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80", category: "kosmos" },
  { id: "space8", name: "Meteor", type: "image", value: "https://images.unsplash.com/photo-1534841090574-cba2d662b62e?w=1920&q=80", category: "kosmos" },
  { id: "space9", name: "Astronavt", type: "image", value: "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1920&q=80", category: "kosmos" },
  { id: "space10", name: "Koinot", type: "image", value: "https://images.unsplash.com/photo-1465101162946-4377e57745c3?w=1920&q=80", category: "kosmos" },
  { id: "space11", name: "Shimol yog'dusi", type: "image", value: "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=1920&q=80", category: "kosmos" },
  { id: "space12", name: "Qora tuynuk", type: "image", value: "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=1920&q=80", category: "kosmos" },
  
  // Cars
  { id: "car1", name: "Sport mashina", type: "image", value: "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=1920&q=80", category: "mashina" },
  { id: "car2", name: "Klassik", type: "image", value: "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=1920&q=80", category: "mashina" },
  { id: "car3", name: "Superkar", type: "image", value: "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1920&q=80", category: "mashina" },
  { id: "car4", name: "Elektromobil", type: "image", value: "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=1920&q=80", category: "mashina" },
  { id: "car5", name: "Retro", type: "image", value: "https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=1920&q=80", category: "mashina" },
  { id: "car6", name: "Mototsikl", type: "image", value: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920&q=80", category: "mashina" },
  { id: "car7", name: "Formula 1", type: "image", value: "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=1920&q=80", category: "mashina" },
  { id: "car8", name: "SUV", type: "image", value: "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=1920&q=80", category: "mashina" },
  { id: "car9", name: "Lambo", type: "image", value: "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=1920&q=80", category: "mashina" },
  { id: "car10", name: "Ferrari", type: "image", value: "https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=1920&q=80", category: "mashina" },
  
  // Abstract/Art
  { id: "art1", name: "Abstrakt", type: "image", value: "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=1920&q=80", category: "san'at" },
  { id: "art2", name: "Neon", type: "image", value: "https://images.unsplash.com/photo-1550684376-efcbd6e3f031?w=1920&q=80", category: "san'at" },
  { id: "art3", name: "Geometriya", type: "image", value: "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?w=1920&q=80", category: "san'at" },
  { id: "art4", name: "Rangli to'lqin", type: "image", value: "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1920&q=80", category: "san'at" },
  { id: "art5", name: "Minimalist", type: "image", value: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=1920&q=80", category: "san'at" },
  { id: "art6", name: "3D shakl", type: "image", value: "https://images.unsplash.com/photo-1614850523459-c2f4c699c52e?w=1920&q=80", category: "san'at" },
  { id: "art7", name: "Holografik", type: "image", value: "https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?w=1920&q=80", category: "san'at" },
  { id: "art8", name: "Suyuq rang", type: "image", value: "https://images.unsplash.com/photo-1604076913837-52ab5629fba9?w=1920&q=80", category: "san'at" },
  { id: "art9", name: "Pixel", type: "image", value: "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=1920&q=80", category: "san'at" },
  { id: "art10", name: "Gradient", type: "image", value: "https://images.unsplash.com/photo-1557682250-33bd709cbe85?w=1920&q=80", category: "san'at" },
  
  // City
  { id: "city1", name: "Tungi shahar", type: "image", value: "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=1920&q=80", category: "shahar" },
  { id: "city2", name: "Skyline", type: "image", value: "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1920&q=80", category: "shahar" },
  { id: "city3", name: "Ko'prik", type: "image", value: "https://images.unsplash.com/photo-1514565131-fce0801e5785?w=1920&q=80", category: "shahar" },
  { id: "city4", name: "Tokyo", type: "image", value: "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1920&q=80", category: "shahar" },
  { id: "city5", name: "Dubai", type: "image", value: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=1920&q=80", category: "shahar" },
  { id: "city6", name: "New York", type: "image", value: "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1920&q=80", category: "shahar" },
  { id: "city7", name: "London", type: "image", value: "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=1920&q=80", category: "shahar" },
  { id: "city8", name: "Paris", type: "image", value: "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1920&q=80", category: "shahar" },
  { id: "city9", name: "Istanbul", type: "image", value: "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1920&q=80", category: "shahar" },
  { id: "city10", name: "Singapur", type: "image", value: "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=1920&q=80", category: "shahar" },
  
  // Anime/Gaming
  { id: "anime1", name: "Anime osmon", type: "image", value: "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=1920&q=80", category: "oyin" },
  { id: "anime2", name: "Cyberpunk", type: "image", value: "https://images.unsplash.com/photo-1605106702734-205df224ecce?w=1920&q=80", category: "oyin" },
  { id: "anime3", name: "Gaming", type: "image", value: "https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=1920&q=80", category: "oyin" },
  { id: "anime4", name: "Retro gaming", type: "image", value: "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1920&q=80", category: "oyin" },
  { id: "anime5", name: "VR", type: "image", value: "https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=1920&q=80", category: "oyin" },
  { id: "anime6", name: "Esports", type: "image", value: "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1920&q=80", category: "oyin" },
  { id: "anime7", name: "Controller", type: "image", value: "https://images.unsplash.com/photo-1493711662062-fa541f7f3d24?w=1920&q=80", category: "oyin" },
  { id: "anime8", name: "RGB", type: "image", value: "https://images.unsplash.com/photo-1598550476439-6847785fcea6?w=1920&q=80", category: "oyin" },
  
  // Technology
  { id: "tech1", name: "Kod", type: "image", value: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1920&q=80", category: "texnologiya" },
  { id: "tech2", name: "AI chip", type: "image", value: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1920&q=80", category: "texnologiya" },
  { id: "tech3", name: "Server", type: "image", value: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=1920&q=80", category: "texnologiya" },
  { id: "tech4", name: "Robot", type: "image", value: "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1920&q=80", category: "texnologiya" },
  { id: "tech5", name: "Hologram", type: "image", value: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=1920&q=80", category: "texnologiya" },
  { id: "tech6", name: "Circuit", type: "image", value: "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=1920&q=80", category: "texnologiya" },
  { id: "tech7", name: "Data", type: "image", value: "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=1920&q=80", category: "texnologiya" },
  { id: "tech8", name: "Network", type: "image", value: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80", category: "texnologiya" },
  
  // Animals
  { id: "animal1", name: "Sher", type: "image", value: "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=1920&q=80", category: "hayvon" },
  { id: "animal2", name: "Qush", type: "image", value: "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=1920&q=80", category: "hayvon" },
  { id: "animal3", name: "Baliq", type: "image", value: "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1920&q=80", category: "hayvon" },
  { id: "animal4", name: "Fil", type: "image", value: "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=1920&q=80", category: "hayvon" },
  { id: "animal5", name: "Bo'ri", type: "image", value: "https://images.unsplash.com/photo-1474511320723-9a56873571b7?w=1920&q=80", category: "hayvon" },
  { id: "animal6", name: "Ot", type: "image", value: "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=1920&q=80", category: "hayvon" },
  { id: "animal7", name: "Burgut", type: "image", value: "https://images.unsplash.com/photo-1611689342806-0863700ce1e4?w=1920&q=80", category: "hayvon" },
  { id: "animal8", name: "Delfin", type: "image", value: "https://images.unsplash.com/photo-1570481662006-a3a1374699e8?w=1920&q=80", category: "hayvon" },
  
  // Food
  { id: "food1", name: "Qahva", type: "image", value: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1920&q=80", category: "ovqat" },
  { id: "food2", name: "Meva", type: "image", value: "https://images.unsplash.com/photo-1519996529931-28324d5a630e?w=1920&q=80", category: "ovqat" },
  { id: "food3", name: "Shirinlik", type: "image", value: "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=1920&q=80", category: "ovqat" },
  { id: "food4", name: "Burger", type: "image", value: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=1920&q=80", category: "ovqat" },
  
  // Sports
  { id: "sport1", name: "Futbol", type: "image", value: "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=1920&q=80", category: "sport" },
  { id: "sport2", name: "Basketbol", type: "image", value: "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=1920&q=80", category: "sport" },
  { id: "sport3", name: "Tennis", type: "image", value: "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=1920&q=80", category: "sport" },
  { id: "sport4", name: "Suzish", type: "image", value: "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=1920&q=80", category: "sport" },
  
  // Music
  { id: "music1", name: "Gitara", type: "image", value: "https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=1920&q=80", category: "musiqa" },
  { id: "music2", name: "Konsert", type: "image", value: "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=1920&q=80", category: "musiqa" },
  { id: "music3", name: "DJ", type: "image", value: "https://images.unsplash.com/photo-1571266028243-e4733b0f0bb0?w=1920&q=80", category: "musiqa" },
  { id: "music4", name: "Pianino", type: "image", value: "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=1920&q=80", category: "musiqa" },
]

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light")
  const [backgroundTheme, setBackgroundTheme] = useState<BackgroundTheme>(defaultBackground)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const savedTheme = localStorage.getItem("theme") as Theme
    const savedBg = localStorage.getItem("backgroundTheme")
    
    if (savedTheme) {
      setTheme(savedTheme)
      document.documentElement.classList.toggle("dark", savedTheme === "dark")
    } else {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
      setTheme(prefersDark ? "dark" : "light")
      document.documentElement.classList.toggle("dark", prefersDark)
    }
    
    if (savedBg) {
      try {
        setBackgroundTheme(JSON.parse(savedBg))
      } catch {
        setBackgroundTheme(defaultBackground)
      }
    }
  }, [])

  useEffect(() => {
    if (mounted) {
      localStorage.setItem("theme", theme)
      document.documentElement.classList.toggle("dark", theme === "dark")
    }
  }, [theme, mounted])

  useEffect(() => {
    if (mounted) {
      localStorage.setItem("backgroundTheme", JSON.stringify(backgroundTheme))
    }
  }, [backgroundTheme, mounted])

  if (!mounted) {
    return null
  }

  return (
    <ThemeContext.Provider value={{ theme, setTheme, backgroundTheme, setBackgroundTheme, backgrounds }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider")
  }
  return context
}

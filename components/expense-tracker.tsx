"use client"

import { useState, useEffect, useRef, useCallback } from "react"
import { useTheme } from "./theme-provider"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { 
  Sun, 
  Moon, 
  Mic, 
  Plus, 
  Minus, 
  Palette,
  ShoppingCart,
  Car,
  Home,
  Utensils,
  Shirt,
  Smartphone,
  Heart,
  GraduationCap,
  Plane,
  Gift,
  Gamepad2,
  Coffee,
  X,
  Trash2,
  Clock
} from "lucide-react"

interface Expense {
  id: string
  amount: number
  category: string
  description: string
  date: Date
  type: "voice" | "text" | "quick"
}

interface Category {
  id: string
  name: string
  icon: React.ReactNode
  color: string
}

const categories: Category[] = [
  { id: "food", name: "Ovqat", icon: <Utensils className="w-4 h-4" />, color: "bg-orange-500" },
  { id: "transport", name: "Transport", icon: <Car className="w-4 h-4" />, color: "bg-blue-500" },
  { id: "shopping", name: "Xarid", icon: <ShoppingCart className="w-4 h-4" />, color: "bg-pink-500" },
  { id: "home", name: "Uy", icon: <Home className="w-4 h-4" />, color: "bg-green-500" },
  { id: "clothes", name: "Kiyim", icon: <Shirt className="w-4 h-4" />, color: "bg-purple-500" },
  { id: "tech", name: "Texnika", icon: <Smartphone className="w-4 h-4" />, color: "bg-cyan-500" },
  { id: "health", name: "Sog'liq", icon: <Heart className="w-4 h-4" />, color: "bg-red-500" },
  { id: "education", name: "Ta'lim", icon: <GraduationCap className="w-4 h-4" />, color: "bg-indigo-500" },
  { id: "travel", name: "Sayohat", icon: <Plane className="w-4 h-4" />, color: "bg-teal-500" },
  { id: "gift", name: "Sovg'a", icon: <Gift className="w-4 h-4" />, color: "bg-amber-500" },
  { id: "entertainment", name: "Ko'ngil", icon: <Gamepad2 className="w-4 h-4" />, color: "bg-rose-500" },
  { id: "cafe", name: "Kafe", icon: <Coffee className="w-4 h-4" />, color: "bg-yellow-600" },
]

const quickAmounts = [1000, 5000, 10000, 20000, 50000, 100000]

// Format number with spaces
function formatNumber(num: number): string {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
}

// Parse formatted number
function parseFormattedNumber(str: string): number {
  return parseInt(str.replace(/\s/g, ""), 10) || 0
}

export function ExpenseTracker() {
  const { theme, setTheme, backgroundTheme, setBackgroundTheme, backgrounds } = useTheme()
  const [balance, setBalance] = useState<number>(0)
  const [balanceInput, setBalanceInput] = useState<string>("")
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [amount, setAmount] = useState<string>("")
  const [description, setDescription] = useState<string>("")
  const [selectedCategory, setSelectedCategory] = useState<string>("food")
  const [isRecording, setIsRecording] = useState(false)
  const [showThemes, setShowThemes] = useState(false)
  const [selectedThemeCategory, setSelectedThemeCategory] = useState<string>("all")
  
  const recognitionRef = useRef<any>(null)
  const categoryScrollRef = useRef<HTMLDivElement>(null)
  const isRecordingRef = useRef(false)
  const isStartingRef = useRef(false)

  // Load data from localStorage
  useEffect(() => {
    const savedBalance = localStorage.getItem("balance")
    const savedExpenses = localStorage.getItem("expenses")
    
    if (savedBalance) {
      setBalance(parseFloat(savedBalance))
      setBalanceInput(formatNumber(parseFloat(savedBalance)))
    }
    
    if (savedExpenses) {
      try {
        const parsed = JSON.parse(savedExpenses)
        setExpenses(parsed.map((e: any) => ({ ...e, date: new Date(e.date) })))
      } catch {
        setExpenses([])
      }
    }
  }, [])

  // Save data to localStorage
  useEffect(() => {
    localStorage.setItem("balance", balance.toString())
    localStorage.setItem("expenses", JSON.stringify(expenses))
  }, [balance, expenses])

  // Ovozli xarajat qo'shish funksiyasi
  const addVoiceExpense = useCallback((voiceAmount: number, voiceDescription: string, voiceCategory: string) => {
    if (voiceAmount <= 0) return
    
    const newExpense: Expense = {
      id: Date.now().toString(),
      amount: voiceAmount,
      category: voiceCategory,
      description: voiceDescription || categories.find(c => c.id === voiceCategory)?.name || "",
      date: new Date(),
      type: "voice"
    }
    
    setExpenses(prev => [newExpense, ...prev])
    setBalance(prev => {
      const newBalance = prev - voiceAmount
      setBalanceInput(formatNumber(newBalance))
      return newBalance
    })
    setAmount("")
    setDescription("")
  }, [])

  // Initialize speech recognition - kuchli algoritm
  useEffect(() => {
    if (typeof window === "undefined") return
    
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SpeechRecognition) {
      return
    }

    const recognition = new SpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.maxAlternatives = 5
    
    // O'zbekcha birinchi, keyin ruscha va inglizcha
    const tryLanguages = ["uz-UZ", "uz", "ru-RU", "en-US"]
    let currentLangIndex = 0
    recognition.lang = tryLanguages[currentLangIndex]
    
    // Agar til qo'llab-quvvatlanmasa keyingisiga o'tish
    recognition.onerror = (event: any) => {
      if (event.error === "language-not-supported" && currentLangIndex < tryLanguages.length - 1) {
        currentLangIndex++
        recognition.lang = tryLanguages[currentLangIndex]
      } else if (event.error === "not-allowed") {
        alert("Mikrofonga ruxsat berilmadi. Brauzer sozlamalaridan mikrofonga ruxsat bering.")
      }
    }
    
    let pendingText = ""
    let pendingAmount = 0
    let pendingCategory = "food"
    let processTimeout: NodeJS.Timeout | null = null
    
    // Kategoriya kalit so'zlari - O'ZBEKCHA BIRINCHI
    const categoryKeywords: Record<string, string[]> = {
      food: [
        // O'zbekcha
        "ovqat", "yemak", "tushlik", "nonushta", "kechki", "osh", "somsa", "manti", "lagman", "palov", "shurva", 
        "go'sht", "sabzavot", "meva", "oziq", "non", "sut", "tuxum", "guruch", "makaron", "kolbasa", "pishloq",
        "yog'", "shakar", "tuz", "un", "kartoshka", "piyoz", "sabzi", "pomidor", "bodring", "qovun", "tarvuz",
        // Ruscha
        "еда", "обед", "завтрак", "ужин", "кушать", "хлеб", "молоко", "мясо", "рис", "овощи", "фрукты",
        // Inglizcha
        "food", "lunch", "dinner", "breakfast", "meal"
      ],
      transport: [
        // O'zbekcha
        "taksi", "avtobus", "metro", "benzin", "mashina", "yonilg'i", "poyezd", "samolyot", "tramvay", 
        "trolleybus", "yo'l kira", "velosiped", "mototsikl", "avtomobil",
        // Ruscha
        "такси", "бензин", "машина", "транспорт", "автобус", "поезд", "самолет",
        // Inglizcha
        "taxi", "bus", "car", "transport", "uber", "yandex"
      ],
      shopping: [
        // O'zbekcha
        "xarid", "sotib oldim", "dokon", "magazin", "market", "supermarket", "bozor", "savdo", "olish",
        // Ruscha
        "покупка", "магазин", "базар", "торговля",
        // Inglizcha
        "shop", "buy", "shopping", "store"
      ],
      home: [
        // O'zbekcha
        "uy", "kvartira", "ijara", "kommunal", "elektr", "gaz", "suv", "uy-joy", "ta'mir", "mebel",
        // Ruscha
        "дом", "квартира", "аренда", "коммунал", "ремонт",
        // Inglizcha
        "rent", "home", "apartment", "house"
      ],
      clothes: [
        // O'zbekcha
        "kiyim", "ko'ylak", "shim", "krossovka", "poyafzal", "ko'ynak", "palto", "kurtka", "futbolka",
        "sharf", "qalpok", "etik", "tufli", "sumka", "kamar",
        // Ruscha
        "одежда", "обувь", "штаны", "куртка", "платье", "рубашка",
        // Inglizcha
        "clothes", "shoes", "dress", "shirt", "pants"
      ],
      tech: [
        // O'zbekcha
        "telefon", "kompyuter", "noutbuk", "planshet", "quloqchin", "naushnik", "texnika", "televizor",
        "smartfon", "zaryadka", "kabeli", "flesh", "kamera",
        // Ruscha
        "телефон", "компьютер", "ноутбук", "наушники", "техника",
        // Inglizcha
        "phone", "computer", "tech", "laptop", "tablet"
      ],
      health: [
        // O'zbekcha
        "dori", "dorixona", "vrach", "shifokor", "kasalxona", "apteka", "davolash", "tibbiy", "sog'liq",
        "vitamin", "ukol", "tabletkalar",
        // Ruscha
        "аптека", "врач", "лекарство", "больница", "здоровье",
        // Inglizcha
        "medicine", "doctor", "health", "pharmacy", "hospital"
      ],
      education: [
        // O'zbekcha
        "ta'lim", "kurs", "kitob", "darslik", "maktab", "universitet", "o'qish", "dars", "repetitor",
        "ingliz tili", "matematika",
        // Ruscha
        "учеба", "книга", "курс", "школа", "университет",
        // Inglizcha
        "school", "book", "education", "course", "study"
      ],
      travel: [
        // O'zbekcha
        "sayohat", "mehmonxona", "dam olish", "turizm", "aviachiptalar", "viza", "sayyohlik",
        // Ruscha
        "отдых", "отель", "путешествие", "гостиница", "туризм",
        // Inglizcha
        "travel", "hotel", "vacation", "trip", "tourism"
      ],
      gift: [
        // O'zbekcha
        "sovg'a", "tug'ilgan kun", "bayram", "to'y", "hadya", "esdalik",
        // Ruscha
        "подарок", "праздник", "день рождения", "свадьба",
        // Inglizcha
        "gift", "birthday", "present", "wedding"
      ],
      entertainment: [
        // O'zbekcha
        "kino", "teatr", "konsert", "o'yin", "ko'ngilochar", "park", "attraktsion", "muzey",
        // Ruscha
        "кино", "игра", "театр", "концерт", "развлечение",
        // Inglizcha
        "movie", "game", "fun", "entertainment", "cinema"
      ],
      cafe: [
        // O'zbekcha
        "qahva", "choy", "kafe", "restoran", "oshxona", "fastfud", "pitsseriya", "bar",
        // Ruscha
        "кофе", "кафе", "ресторан", "чай", "бар",
        // Inglizcha
        "coffee", "cafe", "restaurant", "tea", "bar"
      ]
    }
    
    const detectCategory = (text: string): string => {
      const lowerText = text.toLowerCase()
      for (const [category, keywords] of Object.entries(categoryKeywords)) {
        for (const keyword of keywords) {
          if (lowerText.includes(keyword)) {
            return category
          }
        }
      }
      return "food"
    }
    
    // KUCHLI RAQAM ANIQLASH ALGORITMI - 0 dan trilliongacha
    const extractAmount = (text: string): number => {
      const originalText = text
      const cleanText = text.toLowerCase().replace(/[''`-]/g, " ").replace(/\s+/g, " ").trim()
      
      // 1. Avval raqamlarni topish (0-9)
      const digitMatches = originalText.match(/\d[\d\s]*/g)
      if (digitMatches) {
        for (const match of digitMatches) {
          const numStr = match.replace(/\s/g, "")
          const parsed = parseInt(numStr, 10)
          if (parsed > 0) {
            console.log("[v0] Raqam topildi:", parsed)
            return parsed
          }
        }
      }
      
      // 2. So'zlardan raqam topish
      // O'zbekcha raqamlar - turli yozilish variantlari
      const wordMap: [RegExp, number][] = [
        // Nol
        [/\b(nol|nul|ноль|нуль)\b/gi, 0],
        // Birliklar
        [/\b(bir|bitta|один|одна|one)\b/gi, 1],
        [/\b(ikki|ikkita|два|две|two)\b/gi, 2],
        [/\b(uch|uchta|у|три|three)\b/gi, 3],
        [/\b(to.?rt|turt|tort|четыре|four)\b/gi, 4],
        [/\b(besh|beshta|пять|five)\b/gi, 5],
        [/\b(olti|oltita|шесть|six)\b/gi, 6],
        [/\b(yetti|yettita|семь|seven)\b/gi, 7],
        [/\b(sakkiz|sakkizta|восемь|eight)\b/gi, 8],
        [/\b(to.?qqiz|tuqqiz|девять|nine)\b/gi, 9],
        // O'nliklar
        [/\b(o.?n|он|десять|ten)\b/gi, 10],
        [/\b(yigirma|двадцать|twenty)\b/gi, 20],
        [/\b(o.?ttiz|utiz|тридцать|thirty)\b/gi, 30],
        [/\b(qirq|kirk|сорок|forty)\b/gi, 40],
        [/\b(ellik|пятьдесят|fifty)\b/gi, 50],
        [/\b(oltmish|шестьдесят|sixty)\b/gi, 60],
        [/\b(yetmish|семьдесят|seventy)\b/gi, 70],
        [/\b(sakson|восемьдесят|eighty)\b/gi, 80],
        [/\b(to.?qson|tuqson|девяносто|ninety)\b/gi, 90],
      ]
      
      // Multiplikatorlar
      const multMap: [RegExp, number][] = [
        [/\b(yuz|сто|сот|hundred)\b/gi, 100],
        [/\b(ming|минг|тысяч|тысячи|тысяча|thousand)\b/gi, 1000],
        [/\b(million|миллион|миллиона|миллионов)\b/gi, 1000000],
        [/\b(milliard|миллиард|миллиарда|миллиардов|billion)\b/gi, 1000000000],
        [/\b(trillion|триллион|триллиона)\b/gi, 1000000000000],
      ]
      
      let foundNumber = 0
      let foundMultiplier = 0
      
      // So'zlarni tekshirish
      for (const [regex, value] of wordMap) {
        if (regex.test(cleanText)) {
          foundNumber += value
          console.log("[v0] So'z topildi:", regex.source, "=", value)
        }
      }
      
      // Multiplikatorlarni tekshirish
      for (const [regex, value] of multMap) {
        if (regex.test(cleanText)) {
          foundMultiplier = Math.max(foundMultiplier, value)
          console.log("[v0] Multiplikator topildi:", regex.source, "=", value)
        }
      }
      
      // Natijani hisoblash
      if (foundMultiplier > 0) {
        if (foundNumber === 0) foundNumber = 1
        const result = foundNumber * foundMultiplier
        console.log("[v0] Natija:", foundNumber, "*", foundMultiplier, "=", result)
        return result
      }
      
      if (foundNumber > 0) {
        console.log("[v0] Faqat raqam:", foundNumber)
        return foundNumber
      }
      
      // 3. Partial match - so'z ichida raqam bormi
      const partialMap: [string, number][] = [
        ["bir", 1], ["ikki", 2], ["uch", 3], ["tort", 4], ["besh", 5],
        ["olti", 6], ["yetti", 7], ["sakkiz", 8], ["toqqiz", 9],
        ["on", 10], ["yigirma", 20], ["ottiz", 30], ["qirq", 40], ["ellik", 50],
        ["ming", 1000], ["yuz", 100],
        ["три", 3], ["два", 2], ["один", 1], ["пять", 5],
        ["тысяч", 1000], ["сто", 100]
      ]
      
      let partialNumber = 0
      let partialMult = 0
      
      for (const [word, value] of partialMap) {
        if (cleanText.includes(word)) {
          if (value >= 100) {
            partialMult = Math.max(partialMult, value)
          } else {
            partialNumber += value
          }
        }
      }
      
      if (partialMult > 0) {
        if (partialNumber === 0) partialNumber = 1
        return partialNumber * partialMult
      }
      
      return partialNumber
    }
    
    recognition.onstart = () => {
      pendingText = ""
      pendingAmount = 0
      pendingCategory = "food"
    }
    
    recognition.onresult = (event: any) => {
      let currentText = ""
      
      for (let i = 0; i < event.results.length; i++) {
        const result = event.results[i]
        let bestText = result[0].transcript
        
        if (result.isFinal) {
          // Eng yaxshi natijani olish
          let bestConfidence = result[0].confidence || 0
          for (let j = 1; j < result.length; j++) {
            if ((result[j].confidence || 0) > bestConfidence) {
              bestConfidence = result[j].confidence
              bestText = result[j].transcript
            }
          }
        }
        currentText += bestText
      }
      
      const trimmedText = currentText.trim()
      if (!trimmedText) return
      
      // UI yangilash
      setDescription(trimmedText)
      
      const detectedAmount = extractAmount(trimmedText)
      if (detectedAmount > 0) {
        setAmount(formatNumber(detectedAmount))
        pendingAmount = detectedAmount
      }
      
      const detectedCategory = detectCategory(trimmedText)
      setSelectedCategory(detectedCategory)
      pendingCategory = detectedCategory
      pendingText = trimmedText
      
      // Timeout orqali avtomatik qo'shish
      if (processTimeout) clearTimeout(processTimeout)
      
      // Agar raqam aniqlansa va mikrofon to'xtatilsa - avtomatik qo'shish
      if (detectedAmount > 0 && event.results[event.results.length - 1]?.isFinal) {
        processTimeout = setTimeout(() => {
          if (pendingAmount > 0 && !isRecordingRef.current) {
            addVoiceExpense(pendingAmount, pendingText, pendingCategory)
            pendingAmount = 0
            pendingText = ""
          }
        }, 500)
      }
    }
    
    recognition.onend = () => {
      // Mikrofon to'xtatilganda - xarajatni qo'shish
      if (pendingAmount > 0 && !isRecordingRef.current) {
        setTimeout(() => {
          if (pendingAmount > 0) {
            addVoiceExpense(pendingAmount, pendingText, pendingCategory)
            pendingAmount = 0
            pendingText = ""
          }
        }, 300)
      }
      
      // Agar hali ham bosib tursa - qayta boshlash
      if (isRecordingRef.current) {
        setTimeout(() => {
          if (isRecordingRef.current && recognitionRef.current) {
            try {
              recognitionRef.current.start()
            } catch (e) {
              // Xato - e'tiborsiz qoldirish
            }
          }
        }, 400)
      }
    }
    
    recognitionRef.current = recognition
    
    return () => {
      if (processTimeout) clearTimeout(processTimeout)
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop()
        } catch (e) {}
      }
    }
  }, [addVoiceExpense])



  const startRecording = useCallback(async () => {
    if (!recognitionRef.current) {
      alert("Brauzeringiz ovozli kiritishni qo'llab-quvvatlamaydi")
      return
    }
    
    // Agar allaqachon ishlayotgan bo'lsa - chiqish
    if (isRecordingRef.current || isStartingRef.current) {
      return
    }
    
    // Mikrofonga ruxsat so'rash
    try {
      await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      })
    } catch (e) {
      alert("Mikrofonga ruxsat berilmadi")
      return
    }
    
    // Avvalgi matnni tozalash
    setDescription("")
    setAmount("")
    
    isStartingRef.current = true
    isRecordingRef.current = true
    setIsRecording(true)
    
    // Recognition boshlash
    try {
      recognitionRef.current.start()
    } catch (e) {
      // Agar xato bo'lsa - to'xtatib qayta boshlash
      try {
        recognitionRef.current.stop()
      } catch (e2) {}
      
      setTimeout(() => {
        if (isRecordingRef.current && recognitionRef.current) {
          try {
            recognitionRef.current.start()
          } catch (e3) {}
        }
        isStartingRef.current = false
      }, 300)
      return
    }
    
    isStartingRef.current = false
  }, [])

  const stopRecording = useCallback(() => {
    isRecordingRef.current = false
    setIsRecording(false)
    
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop()
      } catch (e) {}
    }
  }, [])

  const handleBalanceChange = (value: string) => {
    const numericValue = value.replace(/[^\d]/g, "")
    if (numericValue) {
      const num = parseInt(numericValue, 10)
      setBalance(num)
      setBalanceInput(formatNumber(num))
    } else {
      setBalance(0)
      setBalanceInput("")
    }
  }

  const handleAmountChange = (value: string) => {
    const numericValue = value.replace(/[^\d]/g, "")
    if (numericValue) {
      setAmount(formatNumber(parseInt(numericValue, 10)))
    } else {
      setAmount("")
    }
  }

  const adjustAmount = (delta: number) => {
    const current = parseFormattedNumber(amount)
    const newAmount = Math.max(0, current + delta)
    setAmount(formatNumber(newAmount))
  }

  const addExpense = (type: "voice" | "text" | "quick" = "text") => {
    const expenseAmount = parseFormattedNumber(amount)
    if (expenseAmount <= 0) return

    const newExpense: Expense = {
      id: Date.now().toString(),
      amount: expenseAmount,
      category: selectedCategory,
      description: description || categories.find(c => c.id === selectedCategory)?.name || "",
      date: new Date(),
      type
    }

    setExpenses(prev => [newExpense, ...prev])
    setBalance(prev => prev - expenseAmount)
    setBalanceInput(formatNumber(balance - expenseAmount))
    setAmount("")
    setDescription("")
  }

  const addQuickExpense = (quickAmount: number) => {
    setAmount(formatNumber(quickAmount))
  }

  const deleteExpense = (id: string) => {
    const expense = expenses.find(e => e.id === id)
    if (expense) {
      setBalance(prev => prev + expense.amount)
      setBalanceInput(formatNumber(balance + expense.amount))
      setExpenses(prev => prev.filter(e => e.id !== id))
    }
  }

  const totalSpent = expenses.reduce((sum, e) => sum + e.amount, 0)

  const themeCategories = [
    { id: "all", name: "Hammasi" },
    { id: "solid", name: "Ranglar" },
    { id: "tabiyat", name: "Tabiyat" },
    { id: "kosmos", name: "Kosmos" },
    { id: "mashina", name: "Mashina" },
    { id: "san'at", name: "San'at" },
    { id: "shahar", name: "Shahar" },
    { id: "oyin", name: "O'yin" },
    { id: "texnologiya", name: "Texnologiya" },
    { id: "hayvon", name: "Hayvon" },
    { id: "ovqat", name: "Ovqat" },
    { id: "sport", name: "Sport" },
    { id: "musiqa", name: "Musiqa" },
  ]

  const filteredBackgrounds = selectedThemeCategory === "all" 
    ? backgrounds 
    : backgrounds.filter(bg => bg.category === selectedThemeCategory)

  const formatDate = (date: Date) => {
    return new Intl.DateTimeFormat("uz-UZ", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    }).format(new Date(date))
  }

  return (
    <div className="min-h-screen w-full relative overflow-hidden">
      {/* Background */}
      {backgroundTheme.type === "image" ? (
        <div 
          className="fixed inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${backgroundTheme.value})` }}
        />
      ) : (
        <div className={`fixed inset-0 ${backgroundTheme.value}`} />
      )}
      
      {/* Main Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between p-3 pt-2">
          <h1 className="text-lg font-bold text-card-foreground bg-card/90 px-3 py-1 rounded-full">
            Sarfim
          </h1>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="icon"
              className="rounded-full bg-card/90 border-0 w-9 h-9"
              onClick={() => setShowThemes(true)}
            >
              <Palette className="w-4 h-4" />
            </Button>
            <Button
              variant="outline"
              size="icon"
              className="rounded-full bg-card/90 border-0 w-9 h-9"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
              {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </Button>
          </div>
        </header>

        {/* Balance Section - Compact */}
        <div className="px-4 py-2">
          <div className="bg-card/90 rounded-2xl p-3 shadow-lg">
            <div className="text-center">
              <p className="text-xs text-muted-foreground mb-1">Balansim</p>
              <Input
                type="text"
                value={balanceInput}
                onChange={(e) => handleBalanceChange(e.target.value)}
                placeholder="0"
                className="text-2xl font-bold text-center border-0 bg-transparent h-auto p-0 focus-visible:ring-0"
              />
              <p className="text-xs text-muted-foreground">so'm</p>
            </div>
            <div className="flex justify-between mt-2 pt-2 border-t border-border/50 text-xs">
              <span className="text-muted-foreground">Sarflangan:</span>
              <span className="font-semibold text-destructive">{formatNumber(totalSpent)} so'm</span>
            </div>
          </div>
        </div>

        {/* Categories - Horizontal Scroll */}
        <div className="px-4 py-2">
          <div 
            ref={categoryScrollRef}
            className="flex gap-2 overflow-x-auto hide-scrollbar pb-1"
          >
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`flex flex-col items-center gap-1 min-w-[56px] p-2 rounded-xl transition-all ${
                  selectedCategory === cat.id 
                    ? "bg-card shadow-lg scale-105" 
                    : "bg-card/70"
                }`}
              >
                <div className={`w-8 h-8 rounded-full ${cat.color} flex items-center justify-center text-white`}>
                  {cat.icon}
                </div>
                <span className="text-[10px] font-medium text-card-foreground whitespace-nowrap">{cat.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Amount Input Section */}
        <div className="px-4 py-2 space-y-2">
          {/* Amount with +/- buttons */}
          <div className="bg-card/90 rounded-xl p-3 shadow-lg">
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="icon"
                className="rounded-full w-10 h-10 bg-destructive/10 border-destructive/30 text-destructive hover:bg-destructive/20"
                onClick={() => adjustAmount(-1000)}
              >
                <Minus className="w-5 h-5" />
              </Button>
              <Input
                type="text"
                value={amount}
                onChange={(e) => handleAmountChange(e.target.value)}
                placeholder="Summa kiriting"
                className="text-center text-xl font-bold flex-1 border-0 bg-transparent focus-visible:ring-0"
              />
              <Button
                variant="outline"
                size="icon"
                className="rounded-full w-10 h-10 bg-success/10 border-success/30 text-green-600 hover:bg-success/20"
                onClick={() => adjustAmount(1000)}
              >
                <Plus className="w-5 h-5" />
              </Button>
            </div>
            
            {/* Quick amounts */}
            <div className="flex flex-wrap gap-1.5 mt-2 justify-center">
              {quickAmounts.map((qa) => (
                <button
                  key={qa}
                  onClick={() => addQuickExpense(qa)}
                  className="px-2.5 py-1 bg-secondary rounded-lg text-xs font-medium hover:bg-secondary/80 transition-colors text-secondary-foreground"
                >
                  {formatNumber(qa)}
                </button>
              ))}
            </div>
          </div>

          {/* Description and Mic */}
          <div className="flex gap-2">
            <div className="flex-1 bg-card/90 rounded-xl shadow-lg overflow-hidden">
              <Input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Izoh yozing..."
                className="border-0 bg-transparent focus-visible:ring-0 h-12"
              />
            </div>
            <button
              onMouseDown={startRecording}
              onMouseUp={stopRecording}
              onMouseLeave={stopRecording}
              onTouchStart={startRecording}
              onTouchEnd={stopRecording}
              className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all shadow-lg ${
                isRecording 
                  ? "bg-destructive text-white scale-110 animate-pulse" 
                  : "bg-card/90 text-card-foreground hover:bg-card"
              }`}
            >
              <Mic className="w-5 h-5" />
            </button>
          </div>

          {/* Add button */}
          <Button
            onClick={() => addExpense("text")}
            disabled={!amount}
            className="w-full h-12 text-base font-semibold rounded-xl bg-primary hover:bg-primary/90"
          >
            <Plus className="w-5 h-5 mr-2" />
            Qo'shish
          </Button>
        </div>

        {/* Expense List */}
        <div className="flex-1 px-4 py-2 overflow-hidden">
          <div className="bg-card/90 rounded-2xl shadow-lg h-full flex flex-col max-h-[40vh] md:max-h-[50vh]">
            <div className="p-3 border-b border-border/50">
              <h2 className="font-semibold text-card-foreground flex items-center gap-2 text-sm">
                <Clock className="w-4 h-4" />
                Xarajatlar tarixi
              </h2>
            </div>
            <div className="flex-1 overflow-y-auto p-2">
              {expenses.length === 0 ? (
                <div className="text-center text-muted-foreground py-8 text-sm">
                  Hali xarajat yo'q
                </div>
              ) : (
                <div className="space-y-2">
                  {expenses.map((expense) => {
                    const cat = categories.find(c => c.id === expense.category)
                    return (
                      <div
                        key={expense.id}
                        className="flex items-center gap-2 p-2 bg-secondary/50 rounded-xl"
                      >
                        <div className={`w-8 h-8 rounded-full ${cat?.color || "bg-gray-500"} flex items-center justify-center text-white flex-shrink-0`}>
                          {cat?.icon || <ShoppingCart className="w-4 h-4" />}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-sm text-card-foreground truncate">
                            {expense.description}
                          </p>
                          <p className="text-[10px] text-muted-foreground">
                            {formatDate(expense.date)}
                          </p>
                        </div>
                        <div className="text-right flex-shrink-0">
                          <p className="font-bold text-destructive text-sm">
                            -{formatNumber(expense.amount)}
                          </p>
                        </div>
                        <button
                          onClick={() => deleteExpense(expense.id)}
                          className="p-1.5 hover:bg-destructive/10 rounded-lg transition-colors flex-shrink-0"
                        >
                          <Trash2 className="w-4 h-4 text-destructive" />
                        </button>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Safe area bottom padding */}
        <div className="h-4" />
      </div>

      {/* Theme Selection Modal */}
      {showThemes && (
        <div className="fixed inset-0 z-50 bg-background">
          <div className="h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border">
              <h2 className="text-lg font-bold text-foreground">Temalar</h2>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setShowThemes(false)}
                className="rounded-full"
              >
                <X className="w-5 h-5" />
              </Button>
            </div>

            {/* Category tabs */}
            <div className="p-2 border-b border-border">
              <div className="flex gap-1.5 overflow-x-auto hide-scrollbar">
                {themeCategories.map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedThemeCategory(cat.id)}
                    className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ${
                      selectedThemeCategory === cat.id
                        ? "bg-primary text-primary-foreground"
                        : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
                    }`}
                  >
                    {cat.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Theme grid */}
            <div className="flex-1 overflow-y-auto p-3">
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                {filteredBackgrounds.map((bg) => (
                  <button
                    key={bg.id}
                    onClick={() => {
                      setBackgroundTheme(bg)
                      setShowThemes(false)
                    }}
                    className={`aspect-[4/3] rounded-xl overflow-hidden border-2 transition-all relative ${
                      backgroundTheme.id === bg.id
                        ? "border-primary ring-2 ring-primary/50 scale-95"
                        : "border-transparent hover:border-primary/50"
                    }`}
                  >
                    {bg.type === "image" ? (
                      <img
                        src={bg.value}
                        alt={bg.name}
                        className="w-full h-full object-cover"
                        loading="lazy"
                      />
                    ) : (
                      <div className={`w-full h-full ${bg.value}`} />
                    )}
                    <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent p-2 pt-6">
                      <p className="text-white text-xs font-medium truncate">{bg.name}</p>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

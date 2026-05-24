import './globals.css'
import { Fraunces, Newsreader, Noto_Serif_SC, JetBrains_Mono } from 'next/font/google'

// Display: Fraunces 变量字体（SOFT/opsz 轴自动激活；weight/style 由 axes 接管）
const fontDisplay = Fraunces({
  subsets: ['latin'],
  axes: ['SOFT', 'opsz'],
  style: ['normal', 'italic'],
  variable: '--font-display',
  display: 'swap'
})

// Body Latin: Newsreader 也是变量字体（opsz 自动激活）
const fontBody = Newsreader({
  subsets: ['latin'],
  style: ['normal', 'italic'],
  variable: '--font-body',
  display: 'swap'
})

// CJK: Noto Serif SC（按需加载，preload: false 避免拖慢 LCP）
const fontCjk = Noto_Serif_SC({
  weight: ['400', '500', '700'],
  variable: '--font-cjk',
  display: 'swap',
  preload: false
})

// Mono: JetBrains Mono，用于代码与数字 tabular 对齐
const fontMono = JetBrains_Mono({
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-mono',
  display: 'swap'
})

export const metadata = {
  title: 'Apple Breeding Atlas — 苹果育种文献与基因问答',
  description: '本科毕业设计 · 整合论文与候选基因的可追溯检索问答系统'
}

export default function RootLayout({ children }) {
  const fontClass = `${fontDisplay.variable} ${fontBody.variable} ${fontCjk.variable} ${fontMono.variable}`
  return (
    <html lang="zh-CN" className={fontClass}>
      <body>{children}</body>
    </html>
  )
}

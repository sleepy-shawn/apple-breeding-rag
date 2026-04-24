import './globals.css'

export const metadata = {
  title: 'Apple Breeding Atlas',
  description: 'Workspace for apple breeding papers, genes, and evidence'
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}

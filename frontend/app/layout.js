export const metadata = {
  title: 'Apple Breeding RAG',
  description: 'RAG assistant for apple breeding papers and gene records'
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}

import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "XDOC: Chẩn đoán bệnh tim mạch và tiểu đường",
  description: "Bài dự thi GDGoC Hackathon",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-900`}>
        <header className="border-b border-gray-700/50 backdrop-blur-sm bg-gray-600/50">
          <nav className="container mx-auto p-4">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                <img src="/logo.png" alt="XDOC Logo" className="h-8 rounded-lg w-auto" />
                <Link href="/" className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#00BFFF] to-blue-500">
                  XDOC
                </Link>
                </div>
              <div className="space-x-8">
                <Link
                  href="/diagnosis/diabetes"
                  className="text-gray-300 hover:text-[#00BFFF] transition-colors"
                >
                  Tiểu Đường
                </Link>
                <Link
                  href="/diagnosis/cardiovascular"
                  className="text-gray-300 hover:text-[#00BFFF] transition-colors"
                >
                  Tim Mạch
                </Link>
              </div>
            </div>
          </nav>
        </header>
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
          {children}
        </div>
      </body>
    </html>
  );
}

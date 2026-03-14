import type { Metadata } from "next";
import Script from "next/script";
import { JetBrains_Mono, Manrope } from "next/font/google";
import "./globals.css";

const modernSans = Manrope({
  variable: "--font-sans",
  subsets: ["latin"],
});

const modernMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AiKO",
  description: "Personal AI Companion",
  icons: {
    icon: "data:image/x-icon;base64,AAABAAEAAAABACAAaAAAARgAAA==",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <Script 
          src="https://cubism.live2d.com/sdk-web/cubismcore/live2dcubismcore.min.js"
          strategy="beforeInteractive"
        />
      </head>
      <body
        className={`${modernSans.variable} ${modernMono.variable} font-sans antialiased`}
      >
        {children}
      </body>
    </html>
  );
}

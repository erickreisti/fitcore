import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="absolute top-0 left-0 w-full z-50 px-8 py-6 flex items-center justify-between text-white bg-linear-to-b from-black/80 to-transparent">
      {/* Logo */}
      <div className="flex-1">
        <Link href="/" className="text-3xl font-bold tracking-tight text-white hover:text-emerald-400 transition-colors">
          FitCore
        </Link>
      </div>

      {/* Center Links */}
      <div className="hidden md:flex gap-10 text-xs font-bold tracking-[0.2em] uppercase items-center justify-center flex-1">
        <Link href="#" className="text-white hover:text-emerald-400 transition-colors flex items-center gap-1.5 group">
          Início <span className="text-emerald-500/50 group-hover:text-emerald-400 transition-colors">&raquo;</span>
        </Link>
        <Link href="#" className="text-white/70 hover:text-white transition-colors flex items-center gap-1.5 group">
          Páginas <span className="text-white/30 group-hover:text-white transition-colors">&raquo;</span>
        </Link>
        <Link href="#" className="text-white/70 hover:text-white transition-colors flex items-center gap-1.5 group">
          Portfólio <span className="text-white/30 group-hover:text-white transition-colors">&raquo;</span>
        </Link>
        <Link href="#" className="text-white/70 hover:text-white transition-colors flex items-center gap-1.5 group">
          Blog <span className="text-white/30 group-hover:text-white transition-colors">&raquo;</span>
        </Link>
        <Link href="#" className="text-white/70 hover:text-white transition-colors flex items-center gap-1.5 group">
          Loja <span className="text-white/30 group-hover:text-white transition-colors">&raquo;</span>
        </Link>
        <Link href="#" className="text-white/70 hover:text-white transition-colors">Contatos</Link>
      </div>

      {/* Right Button */}
      <div className="flex-1 flex justify-end">
        <Link href="#" className="border border-white/20 px-8 py-3 uppercase text-xs tracking-widest font-bold hover:border-emerald-500 hover:text-emerald-400 transition-all duration-300">
          Fale Conosco
        </Link>
      </div>
    </nav>
  );
}

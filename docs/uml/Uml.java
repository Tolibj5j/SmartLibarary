import java.awt.*;
import java.awt.geom.*;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.File;

public class Uml {
    static final float S = 2f;
    static Graphics2D g;
    static BufferedImage img;

    static final Color LINE = new Color(45, 55, 72);
    static final Color UC_FILL = new Color(232, 241, 255);
    static final Color UC_STROKE = new Color(46, 89, 160);
    static final Color HEAD_FILL = new Color(214, 228, 250);
    static final Color BODY_FILL = new Color(250, 252, 255);
    static final Color BOUND_FILL = new Color(248, 249, 251);
    static final Stroke SOLID = new BasicStroke(1.4f);
    static final Stroke DASH = new BasicStroke(1.3f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER, 10f, new float[]{7f, 5f}, 0f);

    static Font font(int style, float size) { return new Font("Noto Sans", style, 12).deriveFont(style, size); }

    static void begin(int w, int h) {
        img = new BufferedImage((int) (w * S), (int) (h * S), BufferedImage.TYPE_INT_RGB);
        g = img.createGraphics();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
        g.scale(S, S);
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, w, h);
        g.setStroke(SOLID);
    }

    static void save(String f) throws Exception { ImageIO.write(img, "png", new File(f)); }

    static void textC(String s, double cx, double cy) {
        FontMetrics fm = g.getFontMetrics();
        g.drawString(s, (float) (cx - fm.stringWidth(s) / 2.0), (float) (cy + (fm.getAscent() - fm.getDescent()) / 2.0));
    }

    static void textL(String s, double x, double cy) {
        FontMetrics fm = g.getFontMetrics();
        g.drawString(s, (float) x, (float) (cy + (fm.getAscent() - fm.getDescent()) / 2.0));
    }

    static void line(double x1, double y1, double x2, double y2) { g.draw(new Line2D.Double(x1, y1, x2, y2)); }

    static void openHead(double sx, double sy, double ex, double ey) {
        double a = Math.atan2(ey - sy, ex - sx), L = 11, w = 0.45;
        Stroke old = g.getStroke();
        g.setStroke(SOLID);
        line(ex, ey, ex - L * Math.cos(a - w), ey - L * Math.sin(a - w));
        line(ex, ey, ex - L * Math.cos(a + w), ey - L * Math.sin(a + w));
        g.setStroke(old);
    }

    static void filledHead(double sx, double sy, double ex, double ey) {
        double a = Math.atan2(ey - sy, ex - sx), L = 11, w = 0.4;
        Path2D p = new Path2D.Double();
        p.moveTo(ex, ey);
        p.lineTo(ex - L * Math.cos(a - w), ey - L * Math.sin(a - w));
        p.lineTo(ex - L * Math.cos(a + w), ey - L * Math.sin(a + w));
        p.closePath();
        g.fill(p);
    }

    // ---------- use case helpers ----------
    static final double UW = 236, UH = 52;

    static void actor(double cx, double y, String name) {
        g.setColor(LINE);
        g.setStroke(new BasicStroke(1.8f));
        g.draw(new Ellipse2D.Double(cx - 11, y, 22, 22));
        line(cx, y + 22, cx, y + 56);
        line(cx - 20, y + 33, cx + 20, y + 33);
        line(cx, y + 56, cx - 16, y + 82);
        line(cx, y + 56, cx + 16, y + 82);
        g.setStroke(SOLID);
        g.setFont(font(Font.BOLD, 15));
        textC(name, cx, y + 100);
    }

    static void usecase(double cx, double cy, String t) {
        Shape e = new Ellipse2D.Double(cx - UW / 2, cy - UH / 2, UW, UH);
        g.setColor(UC_FILL);
        g.fill(e);
        g.setColor(UC_STROKE);
        g.draw(e);
        g.setColor(Color.BLACK);
        g.setFont(font(Font.PLAIN, 14));
        textC(t, cx, cy);
    }

    static double[] ellEdge(double cx, double cy, double px, double py) {
        double dx = px - cx, dy = py - cy;
        double t = 1 / Math.sqrt(Math.pow(dx / (UW / 2), 2) + Math.pow(dy / (UH / 2), 2));
        return new double[]{cx + dx * t, cy + dy * t};
    }

    static void assocUC(double ax, double ay, double ucx, double ucy) {
        double[] e = {ax < ucx ? ucx - UW / 2 : ucx + UW / 2, ucy};
        g.setColor(LINE);
        g.setStroke(SOLID);
        line(ax, ay, e[0], e[1]);
    }

    static void depUC(double[] from, double[] to, String label) {
        double[] s = ellEdge(from[0], from[1], to[0], to[1]);
        double[] e = ellEdge(to[0], to[1], from[0], from[1]);
        g.setColor(LINE);
        g.setStroke(DASH);
        line(s[0], s[1], e[0], e[1]);
        openHead(s[0], s[1], e[0], e[1]);
        g.setStroke(SOLID);
        g.setFont(font(Font.ITALIC, 12));
        g.setColor(new Color(90, 90, 90));
        textC(label, (s[0] + e[0]) / 2, (s[1] + e[1]) / 2 - 11);
    }

    static void useCaseDiagram() throws Exception {
        begin(1420, 990);
        // system boundary
        Shape b = new RoundRectangle2D.Double(270, 40, 880, 920, 16, 16);
        g.setColor(BOUND_FILL);
        g.fill(b);
        g.setColor(LINE);
        g.draw(b);
        g.setFont(font(Font.BOLD, 18));
        textC("SmartLibrary tizimi", 710, 66);

        double[] U1 = {420, 120}, U2 = {420, 195}, U3 = {420, 270}, U4 = {420, 345};
        double[] U5 = {420, 480}, U6 = {420, 560}, U7 = {420, 640}, U8 = {420, 720}, U9 = {420, 800}, U12 = {420, 895};
        double[] U10 = {745, 470}, U11 = {745, 610};
        double[] U16 = {995, 240}, U13 = {995, 315}, U14 = {995, 390}, U15 = {995, 465};
        double[] U17 = {995, 820}, U18 = {995, 895};

        // actors
        double stX = 110, stY = 175, liX = 110, liY = 640, adX = 1310, adY = 300, saX = 1310, saY = 800;
        double[] stA = {stX + 24, stY + 40}, liA = {liX + 24, liY + 40}, adA = {adX - 24, adY + 40}, saA = {saX - 24, saY + 40};

        for (double[] u : new double[][]{U1, U2, U3, U4}) assocUC(stA[0], stA[1], u[0], u[1]);
        for (double[] u : new double[][]{U5, U6, U7, U8, U9, U12}) assocUC(liA[0], liA[1], u[0], u[1]);
        for (double[] u : new double[][]{U16, U13, U14, U15}) assocUC(adA[0], adA[1], u[0], u[1]);
        for (double[] u : new double[][]{U17, U18}) assocUC(saA[0], saA[1], u[0], u[1]);

        depUC(U5, U10, "«include»");
        depUC(U6, U10, "«include»");
        depUC(U11, U6, "«extend»");

        usecase(U1[0], U1[1], "Kitob qidirish");
        usecase(U2[0], U2[1], "Kitobni band qilish");
        usecase(U3[0], U3[1], "Sharh va baho qoldirish");
        usecase(U4[0], U4[1], "Telegram botga ulanish");
        usecase(U5[0], U5[1], "Kitob berish");
        usecase(U6[0], U6[1], "Kitobni qaytarib olish");
        usecase(U7[0], U7[1], "Katalogni yuritish");
        usecase(U8[0], U8[1], "O'quvchini ro'yxatga olish");
        usecase(U9[0], U9[1], "Sharhlarni tasdiqlash");
        usecase(U12[0], U12[1], "Qarzdorlarni ko'rish");
        usecase(U10[0], U10[1], "Shtrix-kodni skanerlash");
        usecase(U11[0], U11[1], "Jarimani hisoblash");
        usecase(U16[0], U16[1], "Xodimlar va sozlamalar");
        usecase(U13[0], U13[1], "Jarimani kechirish");
        usecase(U14[0], U14[1], "Kitobni hisobdan chiqarish");
        usecase(U15[0], U15[1], "Hisobot va qarzdorlar");
        usecase(U17[0], U17[1], "Muassasalarni boshqarish");
        usecase(U18[0], U18[1], "Tariflar va obunalar");

        actor(stX, stY, "O'quvchi");
        actor(liX, liY, "Kutubxonachi");
        actor(adX, adY, "Admin");
        actor(saX, saY, "Super-admin");
        save("usecase.png");
    }

    // ---------- class helpers ----------
    static Rectangle2D cls(String name, String[] attrs, String[] ops, double x, double y, double w) {
        double head = 32, row = 20;
        double h = head + 8 + attrs.length * row + 8 + (ops.length == 0 ? 10 : ops.length * row + 8);
        Rectangle2D r = new Rectangle2D.Double(x, y, w, h);
        g.setColor(BODY_FILL);
        g.fill(r);
        g.setColor(HEAD_FILL);
        g.fill(new Rectangle2D.Double(x, y, w, head));
        g.setColor(LINE);
        g.draw(r);
        line(x, y + head, x + w, y + head);
        double ya = y + head + 8 + attrs.length * row;
        line(x, ya, x + w, ya);
        g.setColor(Color.BLACK);
        g.setFont(font(Font.BOLD, 15));
        textC(name, x + w / 2, y + head / 2);
        g.setFont(font(Font.PLAIN, 13));
        for (int i = 0; i < attrs.length; i++) textL(attrs[i], x + 10, y + head + 8 + row * i + row / 2);
        for (int i = 0; i < ops.length; i++) textL(ops[i], x + 10, ya + 4 + row * i + row / 2);
        return r;
    }

    static double[] rectEdge(Rectangle2D r, double px, double py) {
        double cx = r.getCenterX(), cy = r.getCenterY(), dx = px - cx, dy = py - cy;
        double tx = dx == 0 ? 1e9 : (r.getWidth() / 2) / Math.abs(dx);
        double ty = dy == 0 ? 1e9 : (r.getHeight() / 2) / Math.abs(dy);
        double t = Math.min(tx, ty);
        return new double[]{cx + dx * t, cy + dy * t};
    }

    static void mult(double[] end, double[] other, String m) {
        double dx = other[0] - end[0], dy = other[1] - end[1], len = Math.hypot(dx, dy);
        dx /= len; dy /= len;
        double px = end[0] + dx * 20 - dy * 12, py = end[1] + dy * 20 + dx * 12;
        g.setFont(font(Font.BOLD, 13));
        g.setColor(new Color(150, 40, 40));
        textC(m, px, py);
    }

    static void assoc(Rectangle2D a, Rectangle2D b, String ma, String mb, boolean compositionAtA) {
        double[] pa = rectEdge(a, b.getCenterX(), b.getCenterY());
        double[] pb = rectEdge(b, a.getCenterX(), a.getCenterY());
        g.setColor(LINE);
        g.setStroke(SOLID);
        line(pa[0], pa[1], pb[0], pb[1]);
        if (compositionAtA) {
            double ang = Math.atan2(pb[1] - pa[1], pb[0] - pa[0]);
            Path2D d = new Path2D.Double();
            d.moveTo(0, 0); d.lineTo(10, -6); d.lineTo(20, 0); d.lineTo(10, 6); d.closePath();
            AffineTransform t = new AffineTransform();
            t.translate(pa[0], pa[1]);
            t.rotate(ang);
            g.fill(t.createTransformedShape(d));
        }
        mult(pa, pb, ma);
        mult(pb, pa, mb);
    }

    static void classDiagram() throws Exception {
        begin(1500, 1010);
        double W = 340, A = 50, B = 580, C = 1110;
        Rectangle2D xodim = cls("Xodim", new String[]{"- id: int", "- ism: String", "- telefon: String", "- rol: admin | kutubxonachi", "- parol_hash: String"},
                new String[]{"+ kirish(): bool"}, A, 30, W);
        Rectangle2D muas = cls("Muassasa", new String[]{"- id: int", "- nomi: String", "- qisqa_kod: String", "- turi: String", "- tarif: String", "- holat: sinov | faol | to'xtatilgan"},
                new String[]{}, B, 30, W);
        Rectangle2D oq = cls("O'quvchi", new String[]{"- id: int", "- ism_familiya: String", "- sinf_guruh: String", "- karta_kodi: String", "- telegram_id: int", "- ball: int"},
                new String[]{"+ botgaUlash(kod): bool"}, A, 330, W);
        Rectangle2D kitob = cls("Kitob", new String[]{"- id: int", "- nomi: String", "- muallif: String", "- isbn: String", "- janr: String"},
                new String[]{"+ qidirish(so'z): List"}, C, 330, W);
        Rectangle2D band = cls("BandQilish", new String[]{"- id: int", "- sana: Date", "- navbat_raqami: int", "- holat: String"},
                new String[]{}, B, 270, W);
        Rectangle2D sharh = cls("Sharh", new String[]{"- id: int", "- baho: 1..5", "- matn: String", "- tasdiqlangan: bool"},
                new String[]{}, B, 480, W);
        Rectangle2D jar = cls("Jarima", new String[]{"- id: int", "- turi: ball | pul", "- miqdor: int", "- kechirilgan: bool"},
                new String[]{"+ kechirish(): void"}, A, 760, W);
        Rectangle2D ber = cls("Berish", new String[]{"- id: int", "- berilgan_sana: Date", "- muddat: Date", "- qaytarilgan_sana: Date", "- xodim_id: int"},
                new String[]{"+ qaytarish(): void", "+ kechikishKunlari(): int"}, B, 740, W);
        Rectangle2D nusxa = cls("Nusxa", new String[]{"- id: int", "- shtrix_kod: String", "- holat: bo'sh | berilgan | band"},
                new String[]{}, C, 760, W);

        assoc(muas, xodim, "1", "*", false);
        assoc(muas, oq, "1", "*", false);
        assoc(muas, kitob, "1", "*", false);
        assoc(oq, band, "1", "*", false);
        assoc(kitob, band, "1", "*", false);
        assoc(oq, sharh, "1", "*", false);
        assoc(kitob, sharh, "1", "*", false);
        assoc(kitob, nusxa, "1", "1..*", true);
        assoc(oq, ber, "1", "*", false);
        assoc(nusxa, ber, "1", "*", false);
        assoc(ber, jar, "1", "0..1", false);
        save("class.png");
    }

    // ---------- sequence ----------
    static double[] X = {90, 300, 535, 770, 1000, 1210};

    static void msg(int a, int b, double y, String t, boolean ret) {
        double x1 = X[a], x2 = X[b];
        g.setColor(LINE);
        g.setStroke(ret ? DASH : SOLID);
        double ex = x2 + (x2 > x1 ? -1 : 1);
        line(x1, y, ex, y);
        g.setStroke(SOLID);
        if (ret) openHead(x1, y, ex, y); else filledHead(x1, y, ex, y);
        g.setFont(font(Font.PLAIN, 13));
        g.setColor(Color.BLACK);
        textC(t, (x1 + x2) / 2, y - 11);
    }

    static void seqHead(int i, String name, boolean isActor, double y) {
        if (isActor) { actor(X[i], y, name); return; }
        Rectangle2D r = new Rectangle2D.Double(X[i] - 92, y + 20, 184, 46);
        g.setColor(HEAD_FILL);
        g.fill(r);
        g.setColor(LINE);
        g.draw(r);
        g.setColor(Color.BLACK);
        g.setFont(font(Font.BOLD, 14));
        textC(name, X[i], y + 43);
    }

    static void sequenceDiagram() throws Exception {
        int H = 960;
        begin(1310, H);
        String[] names = {"Kutubxonachi", "Veb-sayt", "Server (Django)", "Ma'lumotlar bazasi", "Telegram bot", "O'quvchi"};
        boolean[] act = {true, false, false, false, false, true};
        double top = 20, lifeStart = 130, lifeEnd = H - 30;
        g.setColor(new Color(130, 130, 130));
        g.setStroke(DASH);
        for (double x : X) line(x, lifeStart, x, lifeEnd);
        g.setStroke(SOLID);

        double y = 175, d = 44;
        msg(0, 1, y, "1. O'quvchi kartasini skanerlaydi", false); y += d;
        msg(1, 2, y, "2. GET /oquvchilar/{karta}", false); y += d;
        msg(2, 3, y, "3. O'quvchi va qarzlarini so'rash", false); y += d;
        msg(3, 2, y, "4. o'quvchi ma'lumoti", true); y += d;
        msg(2, 1, y, "5. ism, qarzlar soni", true); y += d;
        msg(0, 1, y, "6. Kitob shtrix-kodini skanerlaydi", false); y += d;
        msg(1, 2, y, "7. POST /berish", false); y += d;
        msg(2, 3, y, "8. Nusxa holatini tekshirish", false); y += d;
        msg(3, 2, y, "9. holat", true); y += d;

        // alt fragment
        double fx = 200, fw = 1095, fy = y - 6;
        y += 34;
        msg(2, 3, y, "10. Berish yozuvini saqlash, muddat qo'yish", false); y += d;
        msg(2, 4, y, "11. Xabar yuborish", false); y += d;
        msg(4, 5, y, "12. \"Kitob berildi, muddat: ...\"", false); y += d;
        msg(2, 1, y, "13. Muvaffaqiyatli", true); y += d;
        double sep = y - 14;
        y += 30;
        msg(2, 1, y, "14. Xato: nusxa band yoki berilgan", true); y += 30;
        double fh = y - fy;
        g.setColor(new Color(60, 60, 60));
        g.setStroke(SOLID);
        g.draw(new Rectangle2D.Double(fx, fy, fw, fh));
        Path2D tab = new Path2D.Double();
        tab.moveTo(fx, fy); tab.lineTo(fx + 46, fy); tab.lineTo(fx + 46, fy + 14); tab.lineTo(fx + 38, fy + 22); tab.lineTo(fx, fy + 22); tab.closePath();
        g.setColor(new Color(235, 235, 235));
        g.fill(tab);
        g.setColor(new Color(60, 60, 60));
        g.draw(tab);
        g.setFont(font(Font.BOLD, 13));
        textL("alt", fx + 8, fy + 11);
        g.setFont(font(Font.ITALIC, 13));
        textL("[nusxa bo'sh]", fx + 56, fy + 12);
        g.setStroke(DASH);
        line(fx, sep, fx + fw, sep);
        g.setStroke(SOLID);
        textL("[nusxa band yoki berilgan]", fx + 8, sep + 13);

        y += 26;
        msg(1, 0, y, "15. Natijani ekranda ko'rsatadi", true);

        for (int i = 0; i < 6; i++) seqHead(i, names[i], act[i], top);
        save("sequence.png");
    }

    public static void main(String[] a) throws Exception {
        useCaseDiagram();
        classDiagram();
        sequenceDiagram();
    }
}

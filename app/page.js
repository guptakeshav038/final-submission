import Link from "next/link";
import MatchAnatomy from "@/components/MatchAnatomy";

export default function Home() {
  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <h1>Match brands with the creators most likely to create value</h1>
          <p className="lead">
            CreatorX scores every brand and creator pair on audience, niche, genuine engagement and location, then shows exactly how the score was built. A creator with 10K active followers can beat one with 500K generic ones.
          </p>
          <div className="cta-row">
            <Link href="/register?role=brand" className="btn">I'm a brand</Link>
            <Link href="/register?role=creator" className="btn btn-ghost">I'm a creator</Link>
          </div>
        </div>
        <MatchAnatomy />
      </section>

      <section className="band">
        <div className="two-col">
          <div>
            <h2>For creators</h2>
            <p>Mid-tier talent gets overlooked, rejections come without reasons, and pricing is a guess. On CreatorX you see which factors drove every match, and brands come to you.</p>
          </div>
          <div>
            <h2>For brands</h2>
            <p>Follower counts hide bot engagement and weak audience fit. CreatorX ranks by verified engagement and demographics against your campaign goal, so vetting takes minutes.</p>
          </div>
        </div>
      </section>

      <section className="band">
        <h2>How a match is made</h2>
        <ol className="steps">
          <li><strong>Brief.</strong> A brand describes the campaign, audience, location and budget.</li>
          <li><strong>Screen.</strong> Creators outside the follower and price limits are filtered out.</li>
          <li><strong>Score.</strong> Each remaining creator is scored on six factors, weighted by the campaign goal.</li>
          <li><strong>Offer.</strong> The brand sends an offer to top matches, and the creator accepts or declines.</li>
        </ol>
      </section>
    </main>
  );
}

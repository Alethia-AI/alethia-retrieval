import clsx from "clsx";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<"svg">>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: "Easy to Use",
    Svg: require("@site/static/img/privocia.svg").default,
    description: (
      <>
        privocia was designed from the ground up to be easily installed and used
        to get your RAG pipeline up and running quickly.
      </>
    ),
  },
  {
    title: "Focus on What Matters",
    Svg: require("@site/static/img/privocia.svg").default,
    description: (
      <>
        privocia lets you focus on your RAG pipeline, and we'll do the chores.
        Go ahead and build your RAG pipeline.
      </>
    ),
  },
  {
    title: "Examples and Demos",
    Svg: require("@site/static/img/privocia.svg").default,
    description: (
      <>
        Check out privocia API in action across multiple frameworks and use
        cases
      </>
    ),
  },
];

function Feature({ title, Svg, description }: FeatureItem) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

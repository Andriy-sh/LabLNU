type Props = Promise<{ id: number }>;
export default async function BookDetails(props: { params: Props }) {
  const resolvedParams = await props.params;
  const { id } = resolvedParams;

  return <div>{id}</div>;
}

# Attribution and adaptation

Original workflows: Anthropic, https://github.com/anthropics/knowledge-work-plugins/tree/33d3dea41a341b341d4f5da2e8801ae0c89be2b8/bio-research.
Source commit: `33d3dea41a341b341d4f5da2e8801ae0c89be2b8`. License: Apache-2.0; see [LICENSE](LICENSE).

This is an unofficial Codex adaptation. The preserved `SOURCE.md`, commands, and `UPSTREAM_CONNECTORS.md` files are original reference material. Generated `SKILL.md` and `CONNECTORS.md` files adapt their use to Codex and do not imply Anthropic endorsement or SaaS connector parity.

Adapted opt-in helper scripts (reviewed upstream preimages):
- `skills/nextflow-development/scripts/utils/ncbi_utils.py`
- `skills/nextflow-development/scripts/sra_geo_fetch.py`

## Package integrity inventory

These SHA256 values check generated files for accidental changes. They are not a signature.

<!-- codex-package-sha256-v1
{
  ".codex-adapter-generated": "01439c518702fcf8c15b6a979e4c3e3e6c60809f04a185139b027ff40827cfb7",
  "CONNECTORS.md": "ce6d460217408b6c6f8d84ed130fe49bf7de18b05c3c02d5e0d7139f48f62f9e",
  "LICENSE": "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30",
  "UPSTREAM_CONNECTORS.md": "b93341c72d9bba976fc5b48f757b051768e23e4837e0b300d468aefda2deee7d",
  "UPSTREAM_README.md": "4346d6d0b6eb124fd2b0d94a1e175265ee1b911fb443107216b147114868789c",
  "plugin.json": "d74ed4698fc638994bd04e533879218e8bda9b93ee38e2983076c251b276bc6c",
  "skills/instrument-data-to-allotrope/LICENSE.txt": "7505b489cc8ad7f16ba08343184320f1583303cfacdb9121b9b756bc073df1ab",
  "skills/instrument-data-to-allotrope/SKILL.md": "60b60825fa6dcdb6465db4cbec45f729d212031e7fb992a7abf25053084a9d96",
  "skills/instrument-data-to-allotrope/SOURCE.md": "6167bf1731e568b63110a8f27e987cfe386f44e64cd2d78d9080d5d7628a79c5",
  "skills/instrument-data-to-allotrope/references/asm_schema_overview.md": "339dc491f567d58535dc7c3db1c4bef143eae53ba964dcaf1995f91c970fd37d",
  "skills/instrument-data-to-allotrope/references/field_classification_guide.md": "de83b5b6a0b16a3b3da2671efe94fb9535081154efdc55955caa3bfaf1bcd604",
  "skills/instrument-data-to-allotrope/references/flattening_guide.md": "4f3602b21e6fd6c3dd384a072b983470133d2b7abe5ec46da60a1ce8b7629aab",
  "skills/instrument-data-to-allotrope/references/supported_instruments.md": "eb9d30845eb05d8366d073883cd967a4ccc40eab18dfc1707c35a4100764c8bd",
  "skills/instrument-data-to-allotrope/requirements.txt": "21433e5a443ee926e059dd51ef4497a208bd2f4ae04f8585205375ca12d2510c",
  "skills/instrument-data-to-allotrope/scripts/convert_to_asm.py": "ac7984666cd18a7a1767209b84dadf19a36b02006bd9390a9579e049814d3e53",
  "skills/instrument-data-to-allotrope/scripts/export_parser.py": "32467ff33bd588520d8a7a0acda12b2ec1b26d8058c6cd48c00ad44797a9d3b5",
  "skills/instrument-data-to-allotrope/scripts/flatten_asm.py": "7ded9de71f82a88a3d9dedadb2713b5d33c9cb4d9a2014401dc6af35f90ef72d",
  "skills/instrument-data-to-allotrope/scripts/validate_asm.py": "bb06708d3d2376fdd5fcca1b189440d0d7a4044b4ac949f85aab69644386ccf7",
  "skills/nextflow-development/LICENSE.txt": "7505b489cc8ad7f16ba08343184320f1583303cfacdb9121b9b756bc073df1ab",
  "skills/nextflow-development/SKILL.md": "ab32a02c8a50ef885cb5f0ea6e2a9853e099c6a5d2d91a7723955deed38a1c41",
  "skills/nextflow-development/SOURCE.md": "f30017df5d499427a701ec6cedfc5c9948ca3bd04ee1a2b6a585a29cd93ad0d7",
  "skills/nextflow-development/references/geo-sra-acquisition.md": "85238c3bf2c43d2ca5ad8c4fb4418927ff3443bf8993813925a188a1c287d170",
  "skills/nextflow-development/references/installation.md": "d214ad4508868ed9fd648ec625e633c2b7629df300a4953a4b89fc6010fa7577",
  "skills/nextflow-development/references/pipelines/atacseq.md": "ca6ca22e409e78be3aa6f0e18de9c255fd5e9ac66c59d71ce214fc4a76849a1b",
  "skills/nextflow-development/references/pipelines/rnaseq.md": "c7b0c59b33d52b62d6ca2a476f1f45c849dc83923773f258a0731ba2b7b7c93a",
  "skills/nextflow-development/references/pipelines/sarek.md": "67fa5ee65022875b95e6181baa3eec67c572d0564d2aa7bb498d85551458c2fa",
  "skills/nextflow-development/references/troubleshooting.md": "f49b6b48590170770d8e0eb69ee9894c3de04d779b0031d0515529f2e7c01450",
  "skills/nextflow-development/scripts/check_environment.py": "ab259534959c86c4bcdb7a4a6d2eab1edf9d47de6e273c2a3ca0eb13e6b61604",
  "skills/nextflow-development/scripts/config/genomes.yaml": "940bd833b87542a25705668a3ba8f157ea25fcb698f654f2d410efd410fa4172",
  "skills/nextflow-development/scripts/config/pipelines/atacseq.yaml": "fb63a0f76fec6b71303e8a58bba8c4c38a56ee533784d438953fe5e394444158",
  "skills/nextflow-development/scripts/config/pipelines/rnaseq.yaml": "8df7b123fc64328aa4b97d047b316cdbaf4622d89684dfd0b6aca5a5da263f5a",
  "skills/nextflow-development/scripts/config/pipelines/sarek.yaml": "03a904ab4a5f3de216200b60646f58faa37416d4bafda6289fcca91caf1c4f2f",
  "skills/nextflow-development/scripts/detect_data_type.py": "b69c0293c00f292b27e00b5d36629469e843e60f952d299ce85845fbf258314b",
  "skills/nextflow-development/scripts/generate_samplesheet.py": "14a4acb03e08369ea9d73de872b20e3578bcd3eec7bbfa03c2df6adcf5eacbf1",
  "skills/nextflow-development/scripts/manage_genomes.py": "d27e36e0c442b081ef7e60d426c037967afec97e441e8fd7ae0a5e436b64e863",
  "skills/nextflow-development/scripts/sra_geo_fetch.py": "d68dc01adca869b8b2d47c497e8301e9fbbfc6108d024aac1ea1132ebb163f8b",
  "skills/nextflow-development/scripts/utils/__init__.py": "4ef421fc4ad6f13aafc0c34e8c92cf3463cebb0c9f7732d2b9ff876c5cd4d89c",
  "skills/nextflow-development/scripts/utils/file_discovery.py": "3540e5411b1bf52e017a1636a127c4f52392f5e888e0ace47361e4c29e3ef380",
  "skills/nextflow-development/scripts/utils/ncbi_utils.py": "83fb3cb59c37f47d6934bf8cc7e1dd16543bbb5c43bab2116df25e16864903ad",
  "skills/nextflow-development/scripts/utils/sample_inference.py": "3f2dcebbc540fa76e9285dd247cb0d6922d4fbe2588b7f7b3ad7ac7ab82b63af",
  "skills/nextflow-development/scripts/utils/validators.py": "2572671195244a3ac7e67a6ebe4c44bbd541fbaa1afe3ebab1f81a46b29feea1",
  "skills/scientific-problem-selection/LICENSE.txt": "7505b489cc8ad7f16ba08343184320f1583303cfacdb9121b9b756bc073df1ab",
  "skills/scientific-problem-selection/SKILL.md": "5a355e14322937cc01b05225dbe6f25dbb2571b7e74765c6a8545d8fff6418df",
  "skills/scientific-problem-selection/SOURCE.md": "9ec99e3e5b2f4cd7474ef2bb8a1b10ee1f97dbe688c7723c7ec0b18deb8ff0f4",
  "skills/scientific-problem-selection/references/01-intuition-pumps.md": "b29e16c5e55d32ff133aef8ee933cc1abdafae30390f9bb775a8d2e26d129876",
  "skills/scientific-problem-selection/references/02-risk-assessment.md": "4643c7d964060df29c5dc71a41c93e4f6f399fdd4b4f5ffbc3bc5c3919b8a626",
  "skills/scientific-problem-selection/references/03-optimization-function.md": "478641cbcc20e245903543df0d57a86b96e7365eacd2aa61892914488e005bea",
  "skills/scientific-problem-selection/references/04-parameter-strategy.md": "8a286e9e7e21926b7d9e02c50b960f7f9ea03c43542b8ae60c4ce40604966906",
  "skills/scientific-problem-selection/references/05-decision-tree.md": "3a9e164a029b3dc7626f7c3e92978dacca67656e91b5ab60fef21e6381e04f8b",
  "skills/scientific-problem-selection/references/06-adversity-planning.md": "e00b671c3493725339f0bbdb12ad4d876d95f124948ef8ee7c0eb77bf604cda5",
  "skills/scientific-problem-selection/references/07-problem-inversion.md": "19211d825ea39931f2c67b1032f8521462c64a3874116a630aa9e1246d413979",
  "skills/scientific-problem-selection/references/08-integration-synthesis.md": "17e2ddcbb943d2d1053f18b29c858afb91eb3815aa66df3006701ce7659d6189",
  "skills/scientific-problem-selection/references/09-meta-framework.md": "91f4880cef12916d33cf9f12cd42aa23d7cf97f9b9d18e0fb5f0f64e36166602",
  "skills/scvi-tools/LICENSE.txt": "7505b489cc8ad7f16ba08343184320f1583303cfacdb9121b9b756bc073df1ab",
  "skills/scvi-tools/SKILL.md": "2c28696bbc9e80863959079edc02f554ffa1294c3972550c2bb8e453a67e3436",
  "skills/scvi-tools/SOURCE.md": "03a69b32b77db86afe5f87b75db2ae4c92b03b6e9e16e2c5e66cde2d4ad9c5bc",
  "skills/scvi-tools/references/atac_peakvi.md": "9be865ba995796bd2e691df0d49d91039719a4c925b061f1b2a4a044ef6a0316",
  "skills/scvi-tools/references/batch_correction_sysvi.md": "cde389092f5e482ef817a08d08907b6526ddff12e6809333cc5fdab6d8d44d2b",
  "skills/scvi-tools/references/citeseq_totalvi.md": "33fd95d9e435937885a0e0e7f8a3825907a6fbb89a437459a267cd24892521f8",
  "skills/scvi-tools/references/data_preparation.md": "9f67453f39d0ec555540fdc9236a04aef5398e2620417daf987066a68b462027",
  "skills/scvi-tools/references/environment_setup.md": "e262ef9b78fa4d3413eefacdb5d131be4cd16ddf77433daf87aa05eab46dd956",
  "skills/scvi-tools/references/label_transfer.md": "76847bc77975f84c0d5ab00fa13251d85511027cc25c6f76fc671a1b47af0af5",
  "skills/scvi-tools/references/multiome_multivi.md": "f400da4d29456474b8d13e65145b14edb23497ddaf65583ffff5f6967f68dccd",
  "skills/scvi-tools/references/rna_velocity_velovi.md": "ca74c13f859dcd15e1b0389b6a5ff1a2f68113d263a110186057071190a9c20c",
  "skills/scvi-tools/references/scarches_mapping.md": "8afb6c5eb77225f4ac3eaf4e7f18a8fffde5ed1ee46512ff734531afc0ce29f9",
  "skills/scvi-tools/references/scrna_integration.md": "7a04d1fe5a4822be6a395ef4d8e2d528d556fd9a8bcf38e384dbd3da517f93f7",
  "skills/scvi-tools/references/spatial_deconvolution.md": "d7445af2474b22f24ffe8cfff53a445ed5fa43e6cdca31969dfea24018ee54a4",
  "skills/scvi-tools/references/troubleshooting.md": "f74ec705d240ec93acf8127bbf4adf6a6203e24e509ff40a047020d836a5ea1d",
  "skills/scvi-tools/scripts/cluster_embed.py": "eb2f269e15fa1eca1621703631b2848d61655e0eefee65899c082c74f0dcfc47",
  "skills/scvi-tools/scripts/differential_expression.py": "09fff28f11f1650a4179c5a68e32b84b017e54fe5d1f53da766ff3ea4a7a7a01",
  "skills/scvi-tools/scripts/integrate_datasets.py": "f7e3adfd6500cba58617d667745e9101ac953d1c8acc4a5544c788ff9b1e0ba8",
  "skills/scvi-tools/scripts/model_utils.py": "6ce6b43a2b0df4de6253b88fb588373c14504f62d7915d6ef03f295a60313bd4",
  "skills/scvi-tools/scripts/prepare_data.py": "3566b749d45c692bd1ad730de60025675bb1930775048607ff8a59e2e9dd4c67",
  "skills/scvi-tools/scripts/train_model.py": "a0486beaeef3a04799f1b8d06680d56ff9cb5466fa1ea8baa0f2740488947258",
  "skills/scvi-tools/scripts/transfer_labels.py": "4d9f66ef7b3bd682d72b326ba4fec07a9b1ee23e7d8edaad94eb6cac5f333791",
  "skills/scvi-tools/scripts/validate_adata.py": "d72ba68d04ee17c10b7e35eef212ca7b3a8d64327270ab3f24c7bb26d58c14a3",
  "skills/single-cell-rna-qc/LICENSE.txt": "7505b489cc8ad7f16ba08343184320f1583303cfacdb9121b9b756bc073df1ab",
  "skills/single-cell-rna-qc/SKILL.md": "ac4700219b2d65bdafebc45f231f79b709c09bbbfcf0e291280ff6a225144853",
  "skills/single-cell-rna-qc/SOURCE.md": "49cb573916deec6fcf6cc2cb1b573469cbc8c34b84326597ce2db22d0202393f",
  "skills/single-cell-rna-qc/references/scverse_qc_guidelines.md": "a056c4d17d8d39aa9b034aff89e435c5d2371e66470853d3cdff978e34c6fc45",
  "skills/single-cell-rna-qc/scripts/qc_analysis.py": "dbcc2983cacaefffd2369bfae35342fedc22a1ff6415571055e0d9515a85e525",
  "skills/single-cell-rna-qc/scripts/qc_core.py": "24fa2e13fed1b5cecff1f7ed8c5c594314426fd44d418d0526a00480a0c96352",
  "skills/single-cell-rna-qc/scripts/qc_plotting.py": "12bf1a733540817fca963d42deca1b55cc3bd0b6ab26a34472ffd9d344e63c48",
  "skills/start/SKILL.md": "c82cfa480a5635a7b7876b2107590a8fe0c9edc61738df97763cec1107f0b1ab",
  "skills/start/SOURCE.md": "6016fe5c28952feef14ac851134b35b56a1c86614d9163d21fb82205d7e7694b"
}
-->

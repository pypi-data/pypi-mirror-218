# -*- coding: utf-8 -*-

import moto
import pytest

from s3pathlib import S3Path, context

from versioned import exc
from versioned import constants
from versioned.dynamodb import encode_version
from versioned.tests.mock_aws import BaseMockTest
from versioned.core import Repository

from rich import print as rprint


class Test(BaseMockTest):
    use_mock = True

    mock_list = [
        moto.mock_sts,
        moto.mock_s3,
        moto.mock_dynamodb,
    ]

    repo: Repository = None

    @classmethod
    def setup_class_post_hook(cls):
        context.attach_boto_session(cls.bsm.boto_ses)
        cls.repo = Repository(
            aws_region=cls.bsm.aws_region,
            s3_bucket=f"{cls.bsm.aws_account_id}-{cls.bsm.aws_region}-artifacts",
            suffix=".txt",
        )
        cls.repo.bootstrap(cls.bsm)

    def _test(self):
        name = "deploy"
        alias = "LIVE"

        self.repo.purge_artifact(bsm=self.bsm, name=name)

        # ======================================================================
        # Artifact
        # ======================================================================
        # --- test ArtifactNotFoundError ---
        # at this moment, no artifact exists
        with pytest.raises(exc.ArtifactNotFoundError):
            self.repo.publish_artifact_version(bsm=self.bsm, name=name)

        with pytest.raises(exc.ArtifactNotFoundError):
            self.repo.get_artifact_version(bsm=self.bsm, name=name)

        artifact_list = self.repo.list_artifact_versions(bsm=self.bsm, name=name)
        assert len(artifact_list) == 0

        # put artifact
        artifact = self.repo.put_artifact(
            bsm=self.bsm,
            name=name,
            content=b"v1",
            content_type="text/plain",
            metadata={"foo": "bar"},
        )
        # rprint(artifact)
        # put artifact with the same content, S3 and Dynamodb should not changed
        artifact = self.repo.put_artifact(bsm=self.bsm, name=name, content=b"v1")

        def _assert_artifact(artifact):
            assert artifact.name == name
            assert artifact.version == constants.LATEST_VERSION
            assert artifact.s3uri.endswith(constants.LATEST_VERSION + ".txt")
            assert artifact.get_content(bsm=self.bsm) == b"v1"

        _assert_artifact(artifact)

        artifact = self.repo.get_artifact_version(bsm=self.bsm, name=name)
        # rprint(artifact)
        _assert_artifact(artifact)

        artifact_list = self.repo.list_artifact_versions(bsm=self.bsm, name=name)
        # rprint(artifact_list)
        assert len(artifact_list) == 1
        _assert_artifact(artifact_list[0])

        artifact = self.repo.publish_artifact_version(bsm=self.bsm, name=name)
        # rprint(artifact)
        assert artifact.version == "1"
        assert artifact.s3uri.endswith("1".zfill(constants.VERSION_ZFILL) + ".txt")
        assert (
            artifact.s3path.basename == str("1").zfill(constants.VERSION_ZFILL) + ".txt"
        )
        assert artifact.s3path.metadata["foo"] == "bar"
        assert artifact.get_content(bsm=self.bsm) == b"v1"

        # put artifact again
        artifact = self.repo.put_artifact(bsm=self.bsm, name=name, content=b"v2")
        # rprint(artifact)
        assert artifact.version == constants.LATEST_VERSION
        assert S3Path(artifact.s3uri).read_text(bsm=self.bsm) == "v2"

        artifact = self.repo.publish_artifact_version(bsm=self.bsm, name=name)
        # rprint(artifact)
        assert artifact.version == "2"
        s3path = S3Path(artifact.s3uri)
        assert artifact.s3uri.endswith("2".zfill(constants.VERSION_ZFILL) + ".txt")
        assert (
            artifact.s3path.basename == str("2").zfill(constants.VERSION_ZFILL) + ".txt"
        )
        assert artifact.get_content(bsm=self.bsm) == b"v2"

        artifact_list = self.repo.list_artifact_versions(bsm=self.bsm, name=name)
        assert len(artifact_list) == 3

        # ======================================================================
        # Artifact
        # ======================================================================
        # --- test raises error ---
        # try to put alias on non-exist artifact
        with pytest.raises(exc.ArtifactNotFoundError):
            self.repo.put_alias(bsm=self.bsm, name=name, alias=alias, version=999)

        # secondary_version_weight type is wrong
        with pytest.raises(TypeError):
            self.repo.put_alias(
                bsm=self.bsm, name=name, alias=alias, secondary_version=999
            )

        # secondary_version_weight type is wrong
        with pytest.raises(TypeError):
            self.repo.put_alias(
                bsm=self.bsm,
                name=name,
                alias=alias,
                secondary_version=999,
                secondary_version_weight=0.5,
            )

        # secondary_version_weight value range is wrong
        with pytest.raises(ValueError):
            self.repo.put_alias(
                bsm=self.bsm,
                name=name,
                alias=alias,
                secondary_version=999,
                secondary_version_weight=-100,
            )

        # secondary_version_weight value range is wrong
        with pytest.raises(ValueError):
            self.repo.put_alias(
                bsm=self.bsm,
                name=name,
                alias=alias,
                secondary_version=999,
                secondary_version_weight=999,
            )

        # try to put alias on non-exist artifact
        with pytest.raises(exc.ArtifactNotFoundError):
            self.repo.put_alias(
                bsm=self.bsm,
                name=name,
                alias=alias,
                secondary_version=999,
                secondary_version_weight=20,
            )

        # version and secondary_version is the same
        with pytest.raises(ValueError):
            self.repo.put_alias(
                bsm=self.bsm,
                name=name,
                alias=alias,
                version=1,
                secondary_version=1,
                secondary_version_weight=20,
            )

        # alias not exists
        with pytest.raises(exc.AliasNotFoundError):
            self.repo.get_alias(bsm=self.bsm, name=name, alias="Invalid")

        # put alias
        ali = self.repo.put_alias(bsm=self.bsm, name=name, alias=alias)
        # rprint(ali)

        def _assert_alias(ali):
            assert ali.name == name
            assert ali.alias == alias
            assert ali.version == constants.LATEST_VERSION
            assert ali.secondary_version is None
            assert ali.secondary_version_weight is None
            assert ali.version_s3uri.endswith(constants.LATEST_VERSION + ".txt")
            assert ali.secondary_version_s3uri is None
            assert ali.get_version_content(bsm=self.bsm) == b"v2"

        _assert_alias(ali)

        ali = self.repo.get_alias(bsm=self.bsm, name=name, alias=alias)
        # rprint(ali)
        _assert_alias(ali)

        ali_list = self.repo.list_aliases(bsm=self.bsm, name=name)
        assert len(ali_list) == 1
        _assert_alias(ali_list[0])

        # put alias again
        ali = self.repo.put_alias(
            bsm=self.bsm,
            name=name,
            alias=alias,
            version=1,
            secondary_version=2,
            secondary_version_weight=20,
        )
        # rprint(ali)

        def _assert_alias(ali):
            assert ali.name == name
            assert ali.alias == alias
            assert ali.version == "1"
            assert ali.secondary_version == "2"
            assert ali.secondary_version_weight == 20
            assert ali.version_s3uri.endswith(encode_version(1) + ".txt")
            assert ali.secondary_version_s3uri.endswith(encode_version(2) + ".txt")
            assert ali.get_version_content(bsm=self.bsm) == b"v1"
            assert ali.get_secondary_version_content(bsm=self.bsm) == b"v2"

        _assert_alias(ali)

        ali = self.repo.get_alias(bsm=self.bsm, name=name, alias=alias)
        # rprint(ali)
        _assert_alias(ali)

        ali_list = self.repo.list_aliases(bsm=self.bsm, name=name)
        assert len(ali_list) == 1
        _assert_alias(ali_list[0])

        # --- test delete methods
        self.repo.delete_alias(bsm=self.bsm, name=name, alias=alias)
        with pytest.raises(exc.AliasNotFoundError):
            self.repo.get_alias(bsm=self.bsm, name=name, alias=alias)
        ali_list = self.repo.list_aliases(bsm=self.bsm, name=name)
        assert len(ali_list) == 0

        self.repo.delete_artifact_version(bsm=self.bsm, name=name)
        with pytest.raises(exc.ArtifactNotFoundError):
            self.repo.get_artifact_version(bsm=self.bsm, name=name)
        artifact_list = self.repo.list_artifact_versions(bsm=self.bsm, name=name)
        assert len(artifact_list) == 2

        self.repo.delete_artifact_version(bsm=self.bsm, name=name, version=1)
        with pytest.raises(exc.ArtifactNotFoundError):
            self.repo.get_artifact_version(bsm=self.bsm, name=name, version=1)
        artifact_list = self.repo.list_artifact_versions(bsm=self.bsm, name=name)
        assert len(artifact_list) == 1

        # it is a soft delete, so S3 artifact is not deleted
        assert s3path.parent.count_objects(bsm=self.bsm) == 3

        # --- purge
        with pytest.raises(exc.ArtifactNotFoundError):
            self.repo.put_alias(bsm=self.bsm, name=name, alias="DEV", version=1)

        self.repo.put_alias(bsm=self.bsm, name=name, alias="DEV", version=2)
        ali_list = self.repo.list_aliases(bsm=self.bsm, name=name)
        assert len(ali_list) == 1

        self.repo.purge_artifact(bsm=self.bsm, name=name)
        assert s3path.parent.count_objects(bsm=self.bsm) == 0
        artifact_list = self.repo.list_artifact_versions(bsm=self.bsm, name=name)
        assert len(artifact_list) == 0
        ali_list = self.repo.list_aliases(bsm=self.bsm, name=name)
        assert len(ali_list) == 0

    def test(self):
        self._test()


if __name__ == "__main__":
    from versioned.tests import run_cov_test

    run_cov_test(__file__, "versioned.core", preview=False)

package com.example.spring.comment;

import com.example.spring.entity.BoardEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CommentRepository extends JpaRepository<CommentEntity, Integer> {

    @Query("SELECT c from CommentEntity c WHERE c.boardno = :boardno")
    List<CommentEntity> findByBoardno(@Param("boardno") int boardno);

    @Query("SELECT c from CommentEntity c WHERE c.userid = :userid")
    List<CommentEntity> findByUserid(@Param("userid") String userid);


    @Query("UPDATE CommentEntity b SET b.cmtcontent = :cmtcontent WHERE b.boardno = :boardno")
    void update(@Param("boardno") int boardno, @Param("cmtcontent") String cmtcontent);

}

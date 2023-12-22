package com.example.spring.repository;

import com.example.spring.entity.BoardEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BoardRepository extends JpaRepository<BoardEntity, Integer> {
    // 조회수 증가
    @Modifying
    @Query(value = "update BoardEntity b set b.boardcnt = b.boardcnt + 1 where b.boardno = :boardno")
    void updateHit(@Param("boardno") int boardno);

    // 작성자 이름으로 게시글 찾기
    @Query("SELECT b FROM BoardEntity b WHERE b.userid LIKE %:writer%")
    List<BoardEntity> findByWriter(@Param("writer") String writer);


    // 제목으로 게시글 찾기
    @Query("SELECT b from BoardEntity b WHERE b.boardtitle LIKE %:title%")
    List<BoardEntity> findByTitle(@Param("title") String title);
//    @Modifying
//    @Query("UPDATE BoardEntity b SET b.boardtitle = :boardtitle, b.boardcontent = :boardcontent, b.boardfilename = :boardfilename, b.boardfilepath = :boardfilepath WHERE b.boardno = :boardno")
//    void updateFile(@Param("boardno") int boardno,@Param("boardtitle") String boardtitle, @Param("boardcontent") String boardcontent ,@Param("boardfilename") String boardfilename, @Param("boardfilepath") String boardfilepath);
//
//    @Modifying
//    @Query("UPDATE BoardEntity b SET b.boardtitle = :boardtitle, b.boardcontent = :boardcontent WHERE b.boardno = :boardno")
//    void update(@Param("boardno") int boardno, @Param("boardtitle") String boardtitle, @Param("boardcontent") String boardcontent);
//

}

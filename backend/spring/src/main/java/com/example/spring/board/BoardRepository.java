package com.example.spring.board;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface BoardRepository extends JpaRepository<BoardEntity, Integer> {

    // 조회수 증가
    @Modifying
    @Query(value = "update BoardEntity b set b.boardcnt = b.boardcnt + 1 where b.boardno = :boardno")
    void updateHit(@Param("boardno") int boardno);

    
}
